# Лабораторная работа 1. 1. Установка и настройка Docker. Работа с контейнерами в Docker

## Цель работы
Освоить процесс установки и настройки Docker, научиться работать с основными командами CLI, контейнерами и образами. Понять принципы контейнеризации для развертывания аналитических сред и сервисов.

## Ход работы

Проверка версии Docker

<img width="747" height="528" alt="image" src="https://github.com/user-attachments/assets/3b3ae362-4853-4ff6-b15c-2ea6c9862de9" />

Просмотр скачанных образов

<img width="837" height="552" alt="image" src="https://github.com/user-attachments/assets/5a0a98c6-bf90-427b-b126-bfc91cbffb27" />

Просмотр запущенных контейнеров

<img width="830" height="125" alt="image" src="https://github.com/user-attachments/assets/7f1b897c-b369-4f60-94c7-4bbcd290601a" />

Просмотр запущенных контейнеров, включая остановленных

<img width="1053" height="523" alt="image" src="https://github.com/user-attachments/assets/0763bd6b-4592-4f1a-920b-ad6e0b4ac5d7" />

## Индивидуальное задание
### Вариант 18
#### **БД временных рядов.** Используется для IoT и метрик. Запустить контейнер, зайти в веб-интерфейс (порт 8086) и создать первичного пользователя/организацию.

Запуск контейнера influxdb	
**Создаём исполняемый файл с помощью nano influx.sh.**
```
#!/bin/bash

CONTAINER_NAME="influxdb"
PORT="8086"

show_menu() {
    clear
    echo "=========================================="
    echo "       InfluxDB Container Manager"
    echo "=========================================="
    echo "1. Start InfluxDB (Start container)"
    echo "2. Check Status (Check port 8086)"
    echo "3. Stop InfluxDB (Stop container)"
    echo "4. Remove InfluxDB (Remove container)"
    echo "5. Exit"
    echo "=========================================="
    read -p "Select an option (1-5): " choice
}

start_influx() {
    echo "Starting InfluxDB container..."
    docker run -d -p $PORT:8086 --name $CONTAINER_NAME influxdb:latest
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] InfluxDB is starting."
    else
        echo "[ERROR] Failed to start container. Check if Docker is running."
    fi
    read -p "Press enter to continue..."
}

check_status() {
    echo "Checking status on port $PORT..."
    if command -v lsof >/dev/null 2>&1; then
        lsof -i :$PORT
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tuln | grep $PORT
    fi
    
    echo "Listing running containers:"
    docker ps --filter "name=$CONTAINER_NAME"
    read -p "Press enter to continue..."
}

stop_influx() {
    echo "Stopping InfluxDB container..."
    docker stop $CONTAINER_NAME
    read -p "Press enter to continue..."
}

remove_influx() {
    echo "Removing InfluxDB container..."
    docker rm $CONTAINER_NAME
    read -p "Press enter to continue..."
}

while true; do
    show_menu
    case $choice in
        1) start_influx ;;
        2) check_status ;;
        3) stop_influx ;;
        4) remove_influx ;;
        5) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
done
```
Проверка influxdb	на порту 8086 

Создание первичного пользователя

Остановка контейнера, проверка


## Вывод
В ходе выполнения лабораторной работы был изучен функционал Docker, а конкретно: запуск и остановка контейнеров, просмотр образов и запущенных контейнеров.

