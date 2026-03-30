# Отчет по лабораторной работе №3

## Развертывание приложения в Kubernetes

**Студент:** Семеняченко Данил
**Группа:** АДЭУ-221
**Вариант:** 18  
**Задача:** Развернуть аналитическую БД InfluxDB и интерфейс Chronograf для визуализации метрик в кластере Kubernetes.

---

### 1. Цель работы

Освоить процесс оркестрации контейнеров. Научиться разворачивать связки сервисов в кластере Kubernetes, управлять их масштабированием (Deployment) и сетевой доступностью (Service).

### 2. Ход выполнения

#### 2.1. Подготовка манифестов

Для работы были созданы манифесты, описывающие конфигурацию подов, сервисов и секретов. Использовались официальные образы InfluxDB (версия 1.8) и Chronograf.

#### 2.2. Листинг и пояснение YAML-файлов

**1. Секреты (`secrets.yaml`)**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: influxdb-auth
type: Opaque
data:
  # Данные в кодировке base64 для авторизации
  INFLUXDB_ADMIN_USER: YWRtaW4=
  INFLUXDB_ADMIN_PASSWORD: cGFzc3dvcmQ=
```

**2. База данных (`db-deployment.yaml`)**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: influxdb-db
spec:
  selector:
    matchLabels:
      app: influxdb
      tier: storage
  template:
    metadata:
      labels:
        app: influxdb
        tier: storage
    spec:
      containers:
        - name: influxdb
          image: influxdb:1.8
          env:
            - name: INFLUXDB_HTTP_AUTH_ENABLED
              value: "true"
            - name: INFLUXDB_ADMIN_USER
              valueFrom:
                secretKeyRef:
                  name: influxdb-auth
                  key: INFLUXDB_ADMIN_USER
          ports:
            - containerPort: 8086
              name: influxdb
```

**3. Приложение Chronograf (`app-deployment.yaml`)**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chronograf-app
spec:
  selector:
    matchLabels:
      app: chronograf
      tier: frontend
  template:
    metadata:
      labels:
        app: chronograf
        tier: frontend
    spec:
      containers:
        - name: chronograf
          image: chronograf:latest
          env:
            - name: INFLUXDB_URL
              value: http://influxdb-service:8086 # Имя сервиса БД
            - name: INFLUXDB_USERNAME
              valueFrom:
                secretKeyRef:
                  name: influxdb-auth
                  key: INFLUXDB_ADMIN_USER
          ports:
            - containerPort: 8888
              name: chronograf
```

**4. Сетевые интерфейсы (`services.yaml`)**

- `influxdb-service` (ClusterIP): Обеспечивает внутренний доступ к БД для Chronograf.
- `chronograf-service` (NodePort: 30888): Открывает доступ к веб-интерфейсу Chronograf снаружи кластера через порт 30888.

#### 2.3. Проверка взаимодействия

Для проверки работоспособности используются команды:

- `kubectl get pods` — для подтверждения статуса **Running**.
- `kubectl get services` — для проверки корректности проброса портов.

---

### 3. Результаты

**Интерфейс Chronograf (localhost:30888):**
Приложение доступно в браузере. Выполнены настройки подключения к InfluxDB через внутренний DNS-адрес сервиса.

---

### 4. Выводы

Kubernetes позволяет декларативно описывать инфраструктуру и связывать компоненты через абстракции `Service` и `Label`. Использование `NodePort` позволяет легко выносить аналитические инструменты на внешний доступ, а секреты обеспечивают безопасную передачу учетных данных между контейнерами.
