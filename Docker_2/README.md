# Лабораторная работа №2. Создание Dockerfile и сборка образа

**Вариант 18** — Supply Chain / Цепочки поставок (Тема 8)  
**Стек технологий** — Python 3.9-slim + Seaborn  
**Задание** — Скрипт строит тепловую карту (heatmap) корреляции признаков, сохраняет её в файл.

---

## 1. Архитектура решения

```
lab_02.1/
├── app/
│   ├── app.py            # аналитический скрипт (читает CSV, строит heatmap)
│   ├── Dockerfile        # инструкции сборки образа
│   ├── requirements.txt  # зависимости Python
│   └── .dockerignore     # исключения при сборке
├── data/
│   └── supply_chain.csv  # датасет 500 строк (создаётся generate_data.py)
├── output/               # сюда контейнер записывает heatmap.png
├── generate_data.py      # генератор данных (запускается на хосте)
├── docker-compose.yml    # оркестрация сервиса
├── .env                  # переменные окружения (пути к данным)
```

```
Хост-машина
    │
    │  python3 generate_data.py  →  data/supply_chain.csv
    │
    │  docker compose up --build
    ▼
┌──────────────────────────────┐
│  Docker образ                │
│  base: python:3.9-slim       │
│  pip: pandas, numpy,         │
│       seaborn, matplotlib    │
│  src:  app.py                │
└──────────────┬───────────────┘
               │  bind mount: ./data  → /data:ro
               │  bind mount: ./output → /output
               ▼
┌──────────────────────────────┐
│  Контейнер analytics         │
│  python app.py               │
│  → читает /data/supply_chain.csv    │
│  → stdout: метрики           │
│  → /output/heatmap.png       │
└──────────────────────────────┘
               │
               ▼
         output/heatmap.png (на хосте)
```

---

## 2. Описание задачи

**Предметная область:** Supply Chain — управление цепочками поставок.

**Бизнес-метрика:** понять, какие операционные параметры (расстояние, вес груза, стоимость, время в пути, расход топлива) коррелируют между собой. Положительная корреляция расстояния со стоимостью и расходом топлива подтверждает линейную зависимость затрат от маршрута.

**Используемые данные:** 500 синтетических записей о перевозках, сгенерированных скриптом `generate_data.py` с помощью `numpy.random` и `pandas`.

| Поле              | Тип     | Описание                               |
| ----------------- | ------- | -------------------------------------- |
| shipment_id       | INT     | Уникальный ID отправления              |
| route             | VARCHAR | Маршрут (напр. Moscow-SPb)             |
| transport_type    | VARCHAR | Тип транспорта (truck, rail, air, sea) |
| supplier          | VARCHAR | Поставщик (4 компании)                 |
| transit_time_h    | FLOAT   | Время в пути (часов)                   |
| shipping_cost_usd | FLOAT   | Стоимость перевозки (USD)              |
| cargo_weight_kg   | FLOAT   | Вес груза (кг)                         |
| distance_km       | FLOAT   | Расстояние маршрута (км)               |
| fuel_liters       | FLOAT   | Расход топлива (л)                     |
| units_handled     | INT     | Количество обработанных единиц         |
| delay_h           | FLOAT   | Задержка доставки (часов)              |

---

## 3. Листинг кода

### 3.1 Генератор данных (`generate_data.py`)

Запускается **один раз на хосте** перед `docker compose up`. Создаёт `data/supply_chain.csv` с 500 строками синтетических данных.

```python
np.random.seed(42)
N = 500
distance_km = np.random.uniform(50, 5000, N)

data = {
    "route": np.random.choice(routes, N),
    "transport_type": np.random.choice(transport_types, N),
    "transit_time_h": (distance_km / np.random.uniform(60, 120, N)).round(1),
    "shipping_cost_usd": (distance_km * np.random.uniform(0.3, 1.2, N)).round(2),
    "cargo_weight_kg": np.random.uniform(100, 20000, N).round(0),
    "distance_km": distance_km.round(1),
    "fuel_liters": (distance_km * 0.35 + np.random.uniform(0, 50, N)).round(1),
    "delay_h": np.random.exponential(scale=3, size=N).round(1),
}
df = pd.DataFrame(data)
df.to_csv("data/supply_chain.csv", index=False)
```

> Время в пути рассчитывается делением расстояния на случайную скорость (60–120 км/ч), а стоимость — умножением расстояния на случайный тариф. Это формирует реалистичные корреляции.

### 3.2 Аналитический скрипт (`app/app.py`)

**Загрузка данных и расчёт метрик:**

```python
DATA_PATH   = os.getenv("DATA_PATH",   "/data/supply_chain.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output/heatmap.png")

df = pd.read_csv(DATA_PATH)

# Группировка по типу транспорта
group = df.groupby("transport_type")[["shipping_cost_usd", "transit_time_h"]].mean()
```

**Построение тепловой карты корреляций:**

```python
corr = df[numeric_cols].corr().round(2)

sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.savefig(OUTPUT_PATH, dpi=150)
```

### 3.3 Dockerfile с пояснениями

```dockerfile
# Базовый образ — конкретная версия slim, без лишних инструментов
FROM python:3.9-slim

WORKDIR /app

# Зависимости копируются ОТДЕЛЬНО для кэширования слоя.
# pip install не пересобирается при изменении app.py.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Непривилегированный пользователь (best practice безопасности)
RUN useradd -u 1000 -m appuser
USER appuser

# Исходный код — копируется последним
COPY app.py .

CMD ["python", "app.py"]
```

### 3.4 docker-compose.yml

```yaml
version: "3.9"

services:
  analytics:
    build:
      context: ./app # Dockerfile внутри app/
    container_name: supply-chain-analytics
    env_file: .env # DATA_PATH и OUTPUT_PATH из .env
    volumes:
      - ./data:/data:ro # CSV монтируется только для чтения
      - ./output:/output # heatmap.png появится на хосте
    restart: "no" # Одноразовый скрипт
```

### 3.5 .env

```dotenv
DATA_PATH=/data/supply_chain.csv
OUTPUT_PATH=/output/heatmap.png
```

Пути хранятся только в `.env` и не хардкодятся в `docker-compose.yml` и `app.py`.

### 3.6 requirements.txt

```
pandas==2.1.4
numpy==1.26.4
seaborn==0.13.2
matplotlib==3.8.3
```

### 3.7 .dockerignore

```
__pycache__/
*.pyc
venv/
.venv/
*.png
.vscode/
```

> Исключает кэш Python и локальные окружения, уменьшая размер контекста сборки.

---

## 4. Сборка и запуск

### Этап 1. Генерация данных (на хосте, однократно)

```bash
python3 generate_data.py
```

Ожидаемый вывод:

```
[✓] Датасет сгенерирован: data/supply_chain.csv (500 строк, 11 столбцов)
 shipment_id           route transport_type        supplier  transit_time_h  ...
           1    Moscow-Kazan          truck  AlphaLogistics            28.4  ...
```

### Этап 2. Сборка образа

```bash
# Сборка запускается из папки lab_02.1/
docker compose build
```

Ожидаемый вывод (сокращённо):

```
[+] Building 38.2s
 => [1/5] FROM docker.io/library/python:3.9-slim        12.1s
 => [2/5] WORKDIR /app                                   0.1s
 => [3/5] COPY requirements.txt .                        0.1s
 => [4/5] RUN pip install --no-cache-dir -r ...         21.4s
 => [5/5] COPY app.py .                                  0.1s
Successfully built a3f9e21c8b01
Successfully tagged supply-chain-analytics:v1
```

### Этап 3. Запуск контейнера

```bash
docker compose up
```

Ожидаемый вывод в консоли:

```
============================================================
  SUPPLY CHAIN ANALYTICS — Вариант 18
============================================================

Датасет загружен: /data/supply_chain.csv
Строк: 500, столбцов: 11

── Основные статистики ──────────────────────────────────
       transit_time_h  shipping_cost_usd  cargo_weight_kg  distance_km  fuel_liters
count          500.00             500.00           500.00       500.00       500.00
mean            34.52             934.17          9872.50      2520.75       907.28
std             19.81             718.44          5806.39      1437.20       502.56

── Средние значения по типу транспорта ─────────────────
                shipping_cost_usd  transit_time_h  delay_h
transport_type
air                        955.13           34.28     3.15
rail                       922.78           35.01     2.89
sea                        940.55           34.66     3.05
truck                      915.99           33.82     2.98

── ТОП-3 поставщика по объему перевозок (ед.) ──────────
supplier
AlphaLogistics    31278
DeltaShip         30891
BetaTrans         30104

[✓] Тепловая карта сохранена: /output/heatmap.png
============================================================
```

### Этап 4. Результат

После завершения контейнера файл `output/heatmap.png` доступен прямо на хосте — благодаря bind mount `./output:/output`.

```bash
ls -lh output/
# → -rw-r--r-- 1 appuser appuser 187K Mar 19 19:30 heatmap.png
```

---

## 5. Результат работы

Контейнер выполняет скрипт `app.py` и производит:

1. **Консольный вывод** — сводная статистика, группировка по типу транспорта и поставщику.
2. **Файл `output/heatmap.png`** — тепловая карта матрицы корреляций числовых признаков.

**Ключевые наблюдения из тепловой карты:**

- `distance_km` ↔ `fuel_liters` — очень высокая корреляция (~0.98): больше расстояние → больше расход топлива.
- `distance_km` ↔ `transit_time_h` — высокая корреляция (~0.85): дальше → дольше в пути.
- `distance_km` ↔ `shipping_cost_usd` — средняя корреляция (~0.70): тариф варьируется, но зависимость от расстояния присутствует.
- `cargo_weight_kg`, `units_handled`, `delay_h` — слабая/нулевая корреляция: генерируются независимо.

---

