# Лабораторная работа №1. Установка и настройка ETL-инструмента. Создание конвейеров данных

**Цель работы.** Изучение основных принципов работы с ETL-инструментами на примере Pentaho Data Integration (PDI), настройка среды, создание конвейера обработки данных (фильтрация, очистка, замена значений) и выгрузка результатов в базу данных MySQL.

# Задание на лабораторную работу
### Общая задача
1.  Выбрать вариант задания из таблицы ниже.
2.  Скачать CSV-датасет (если ссылка Kaggle недоступна — использовать VPN, найти зеркало, сгенерировать синтетические данные или использовать анонимизированные рабочие данные).
3.  Скачать шаблоны конвейеров для примера: [GitHub Repository](https://github.com/BosenkoTM/workshop-on-ETL/tree/main/lectures/L_01).
4.  Создать трансформацию (`.ktr`), реализующую:
    *   **CSV File Input.** Чтение данных.
    *   **Filter Rows / Value Mapper / String Operations.** Очистка данных, фильтрация битых записей, замена значений.
    *   **Table Output.** Загрузка очищенных данных в таблицу MySQL в базе `mgpu_ico_etl_XX`.
5.  Проверить результат SQL-запросом через phpMyAdmin.

### Варианты заданий
| 18 | Цифровая реклама: обработка данных кампаний. | [Digital Ads Dataset](lab_01/DigitalAd_dataset.csv)

# Выполнение лаборатоной работы

## Созданный конвейер в Spoon (общий вид)

## Настройки ключевых шагов (Input, Filter, Output)

### Настройка блока Input
<img width="1232" height="736" alt="image" src="https://github.com/user-attachments/assets/dd827724-f2c6-49ab-b767-d5875ce6dccf" />

### Настройка блока SelectRows
<img width="1566" height="809" alt="image" src="https://github.com/user-attachments/assets/52ddea72-51aa-4b16-a244-5e22f0e943ac" />

### Настройка блока Filter

###  Настройка блока Calculator

### Настройка блока Output


## SQL-запросы, использованные для проверки загрузки данных, и скриншот результата SELECT из phpMyAdmin

### Для проверки наличия записей использовался такой скрипт: SELECT * FROM `stock_prices` LIMIT 100;


 jTG3yrkc digital_ad_customers
### Для проверки количества записей использовался такой запрос: SELECT COUNT(*) FROM stock_prices;


## Файлы:
[Исходный CSV](lab_01/DigitalAd_dataset.csv)

[Файл трансформации]()

