# Лабораторная работа №3. Комплексное ETL-решение (Вариант 3)

## Цель работы
Разработать решение для интеграции данных из PostgreSQL (база розничных магазинов), Excel (поставки) и CSV (основной склад) в целевое хранилище MySQL, с последующим построением аналитической витрины (View).

## Задание (Вариант 3: Склад)
**Задача:** Создать систему учета остатков. Объединить остатки склада и магазинов, выявить расхождения с поставками. 
**Источники:**
1. PostgreSQL: Розничные магазины (1 000 000 строк).
2. CSV: Основной склад (100 000 строк).
3. Excel: Поставки (100 000 строк).

**Условие фильтрации:** 
Так как целевая таблица MySQL не должна получить весь миллион записей, в процессе ETL (Pentaho) применяется фильтрация: выбираются только записи с критически низким остатком в магазинах (`store_balance < 50`). Это позволяет сократить объем загружаемых данных примерно на 90% (оставив ~100 000 строк), что соответствует заданию. Вычисляется поле `discrepancy` (расхождение): `(store_balance + warehouse_balance) - delivery_qty`.

---

## 1. Архитектура решения
Схема архитектуры разработана с использованием трех слоев:
- **Source Layer:** PostgreSQL, файлы CSV и Excel.
- **Storage Layer:** Staging Area (Pentaho Data Integration) и целевая БД MySQL.
- **Business Layer:** Аналитическое представление (View) в MySQL.

*Файл `architecture.drawio` с разработанной схемой приложен в репозитории. Вы можете открыть его через [draw.io](https://app.diagrams.net/).*

---

## 2. Подготовка данных

### Шаг 2.1. Генерация данных для PostgreSQL
Был подготовлен скрипт (в файле `sql_scripts.sql`), который создает таблицу `retail_stores` и с помощью функции `generate_series` генерирует **1 000 000 строк** случайных данных (ID магазина, ID продукта, остаток, дата и категория товара).
Создание БД:

Наполнение БД:

### Шаг 2.2. Генерация файлов CSV и Excel
Чтобы создать файлы с **100 000 строк**, используется скрипт `generate_data.py` (написан на Python с использованием библиотек `pandas` и `numpy`).
- `main_warehouse.csv` - содержит информацию об остатках на центральном складе (`warehouse_balance`).
- `deliveries.xlsx` - содержит информацию о количестве поставленного товара (`delivery_qty`).

Выполненеи скрипта по генерации данных:


---

## 3. ETL-процесс в Pentaho (Spoon)
Общий вид:
<img width="1499" height="907" alt="image" src="https://github.com/user-attachments/assets/e869763b-8ec7-45dd-bdd1-c904cf716cd6" />
**Table Input:** Чтение данных из PostgreSQL (1 000 000 строк).
<img width="995" height="706" alt="image" src="https://github.com/user-attachments/assets/f1c7451a-8bdd-4e4b-a852-c19c9f1e3744" />

**CSV Input / Excel Input:** Чтение данных из файлов (по 100 000 строк).
<img width="1756" height="729" alt="image" src="https://github.com/user-attachments/assets/a9261bf8-8029-4b98-84a7-f2091bef3841" />

**Stream Lookup:** Обогащение данных из базы данных данными из файлов (присоединение по `product_id`).
<img width="1669" height="564" alt="image" src="https://github.com/user-attachments/assets/73e79646-937e-4084-89f0-64c6f50d8378" />

**Filter Rows:** Фильтрация данных по бизнесс-логике: `store_balance < 50`. Отсеивает около 900 000 строк без критической необходимости в проверке поставок, тем самым защищая MySQL от перегрузки.
<img width="745" height="391" alt="image" src="https://github.com/user-attachments/assets/1c2daf6e-395a-4cf7-b26c-b9aaac4f5440" />

**Calculator:** Расчет расхождения (`discrepancy` = `store_balance` + `warehouse_balance` - `delivery_qty`).
<img width="1544" height="465" alt="image" src="https://github.com/user-attachments/assets/4513cd2d-f9e6-451d-864c-2f45235d7635" />

**Table Output:** Сохранение оставшихся ~100 000 итоговых строк в таблицу `inventory_analysis` в MySQL.
<img width="942" height="882" alt="image" src="https://github.com/user-attachments/assets/1cf90296-d87e-4c45-b198-ffc9996dee6c" />

---

## 4. Бизнес-уровень (Витрина данных)
В MySQL (на основе загруженной таблицы) создается View `view_analytics_report` (скрипт есть в `sql_scripts.sql`), которое группирует данные по категориям и показывает общие суммы остатков, поставок, а также общее отклонение и количество проблемных записей.

БД в MYSQL:
<img width="1553" height="800" alt="image" src="https://github.com/user-attachments/assets/2ade1610-4e90-4317-9ad8-85403a9ebfc1" />

Создание VIEW:
```sql
CREATE OR REPLACE VIEW view_analytics_report AS
SELECT 
    category,
    SUM(store_balance) AS total_store_balance,
    SUM(warehouse_balance) AS total_warehouse_balance,
    SUM(delivery_qty) AS total_delivered,
    SUM(discrepancy) AS total_discrepancy,
    COUNT(*) AS records_analyzed_count
FROM inventory_analysis
GROUP BY category;
```
<img width="1557" height="463" alt="image" src="https://github.com/user-attachments/assets/57d4cc5f-c4d7-442d-a001-e54bf614f3ac" />
Запрос к VIEW:
Категории с наибольшим абсолютным расхождением (discrepancy)
```sql
SELECT 
    category,
    total_discrepancy,
    total_delivered,
    ROUND(total_discrepancy / NULLIF(total_delivered, 0) * 100, 2) AS discrepancy_pct,
    records_analyzed_count
FROM view_analytics_report
WHERE total_delivered > 0
ORDER BY total_discrepancy DESC;
```
<img width="1558" height="739" alt="image" src="https://github.com/user-attachments/assets/3d18cf66-3799-4f93-9b78-ca046cc3f9ee" />

## 5. Вывод
В ходе работы была спроектирована и реализована ETL-архитектура, объединяющая данные из трех различных источников (СУБД и файлы). Была учтена проблема большого объема данных (1 млн записей) путем введения этапа фильтрации в Pentaho, что позволило выделить наиболее приоритетные данные для аналитики и избежать лишней нагрузки на хранилище DWH. Созданы аналитические Business-витрины для пользователей продукта.
