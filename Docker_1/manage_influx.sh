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
