# Инструкция по запуску (MicroK8s)

Так как вы используете **MicroK8s**, вот пошаговый алгоритм запуска приложения из папки проекта:

### 1. Сборка Docker-образов

Соберите образы для бэкенда и фронтенда:

```bash
# Сборка бэкенда
docker build -t membership-backend:latest ./src/backend

# Сборка фронтенда
docker build -t membership-frontend:latest ./src/frontend
```

### 2. Импорт образов в MicroK8s

MicroK8s не видит локальные образы Docker напрямую. Их нужно импортировать во внутреннее хранилище MicroK8s:

```bash
docker save membership-backend:latest | microk8s ctr image import -
docker save membership-frontend:latest | microk8s ctr image import -
```

### 3. Развертывание в Kubernetes

Примените манифест:

```bash
microk8s kubectl apply -f k8s/fullstack.yaml
```

### 4. Проверка статуса

Дождитесь, пока все поды перейдут в состояние `Running`:

```bash
microk8s kubectl get pods
```

### 5. Доступ к приложению

Фронтенд настроен на **NodePort 30080**.
Откройте браузер по адресу:
`http://localhost:30080` (если вы на самой ВМ)
или
`http://<IP_ВАШЕЙ_ВМ>:30080` (если заходите снаружи)
