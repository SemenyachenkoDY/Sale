# Инструкция по проверке работоспособности

> Если у вас нет Docker локально, воспользуйтесь одним из способов ниже.

---

## Способ 1: Виртуальная машина (рекомендуется для лабораторной)

1. Запустите виртуальную машину из образа `dev_kub_student.ova` (VirtualBox / VMware).
2. Перенесите папку `lab_02.1/` на ВМ любым удобным способом:
   - через общую папку VirtualBox,
   - через `scp`, 
   - скопируйте на USB / создайте zip и распакуйте внутри ВМ.
3. Откройте терминал на ВМ и выполните команды:

```bash
# Перейти в папку с проектом
cd lab_02.1/

# Собрать образ (Dockerfile внутри app/)
docker build -t supply-chain-analytics:v1 ./app

# Запустить контейнер (в нём выполнится скрипт и создастся heatmap.png)
docker run --name sc-container supply-chain-analytics:v1

# Скопировать heatmap.png из контейнера на хост
docker cp sc-container:/app/heatmap.png ./heatmap.png

# Убедиться, что файл появился
ls -lh heatmap.png

# Удалить контейнер после проверки
docker rm sc-container
```

---

## Способ 2: Docker Desktop (Windows / Mac)

1. Скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. После установки откройте **PowerShell** и перейдите в папку проекта:

```powershell
cd "C:\Users\Jacku\OneDrive\Рабочий стол\Уник\Продажа\lab_02.1"

# Сборка образа (Dockerfile внутри app/)
docker build -t supply-chain-analytics:v1 ./app

# Запуск
docker run --name sc-container supply-chain-analytics:v1

# Копирование результата
docker cp sc-container:/app/heatmap.png .\heatmap.png

# Очистка
docker rm sc-container
```

---

## Способ 3: Онлайн-среда (без установки)

Используйте [Play With Docker](https://labs.play-with-docker.com/) — бесплатная интерактивная среда с Docker прямо в браузере.

1. Войдите через аккаунт Docker Hub.
2. Нажмите **+ ADD NEW INSTANCE**.
3. Создайте файлы через редактор или загрузите через `git clone`.
4. Выполните команды из Способа 1.

---

## Ожидаемый вывод в консоли

```
============================================================
  SUPPLY CHAIN ANALYTICS — Вариант 18
============================================================

Датасет: 500 записей о перевозках

── Основные статистики ──────────────────────────────────
       transit_time_h  shipping_cost_usd  cargo_weight_kg  ...
count          500.00             500.00           500.00  ...
mean            34.52             934.17          9872.50  ...
std             19.81             718.44          5806.39  ...
min              0.70              21.12           100.00  ...
max             82.30            5896.42         19999.00  ...

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

[✓] Тепловая карта сохранена: /app/heatmap.png
============================================================
```

Файл `heatmap.png` — это матрица корреляций числовых признаков цепочки поставок, сохранённая внутри контейнера.

---

## Проверка образа (опционально)

```bash
# Список всех образов
docker images

# Размер и метаданные образа
docker inspect supply-chain-analytics:v1 | grep -E '"Size"|"Os"'

# История слоёв (можно наглядно увидеть кэширование)
docker history supply-chain-analytics:v1
```
