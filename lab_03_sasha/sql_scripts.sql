
--PgADMIN4
-- Создание исходной таблицы розничных магазинов
CREATE TABLE IF NOT EXISTS retail_stores (
    id SERIAL PRIMARY KEY,
    store_id INT,
    product_id INT,
    store_balance INT,
    date_recorded DATE,
    category VARCHAR(50)
);

-- Генерация 1 000 000 строк синтетических данных
INSERT INTO retail_stores (store_id, product_id, store_balance, date_recorded, category)
SELECT 
    (random() * 50 + 1)::INT,
    (random() * 100000 + 1)::INT,
    (random() * 500)::INT,
    CURRENT_DATE - (random() * 365)::INT,
    CASE (random() * 4)::INT 
        WHEN 0 THEN 'Electronics'
        WHEN 1 THEN 'Clothing'
        WHEN 2 THEN 'Food'
        WHEN 3 THEN 'Furniture'
        ELSE 'Toys'
    END
FROM generate_series(1, 1000000);

--PHP уже все сделано
-- Создание целевой таблицы для хранения обогащенных данных
CREATE TABLE IF NOT EXISTS inventory_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT,                
    screen_id INT,                
    store_id INT,
    product_id INT,
    store_balance INT,
    category VARCHAR(50),
    warehouse_base INT,           
    delivery_qty INT,
    total_stock INT,           
    discrepancy INT
);

-- Создание аналитического представления (View)
CREATE OR REPLACE VIEW view_analytics_report AS
SELECT 
    category,
    SUM(store_balance) AS total_store_balance,
    SUM(warehouse_base) AS total_warehouse_balance,
    SUM(delivery_qty) AS total_delivered,
    SUM(discrepancy) AS total_discrepancy,
    COUNT(*) AS records_analyzed_count
FROM inventory_analysis
GROUP BY category;
