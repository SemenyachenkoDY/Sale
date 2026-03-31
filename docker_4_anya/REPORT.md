# Отчет по лабораторной работе №4.1
## Вариант 18: Membership System (Учет участников клуба/программы)

### 1. Цель работы
Применить полученные знания по созданию и развертыванию трехзвенного приложения (Frontend + Backend + Database) в кластере Kubernetes. Научиться организовывать взаимодействие между микросервисами.

### 2. Описание архитектуры
Приложение состоит из трех основных компонентов:
1.  **Database (PostgreSQL)**: Хранит данные об участниках клуба (ФИО, уровень подписки, дата окончания).
2.  **Backend (FastAPI)**: Предоставляет REST API для выполнения CRUD-операций с базой данных. Обрабатывает запросы от фронтенда и взаимодействует с Postgres через SQLAlchemy.
3.  **Frontend (Streamlit)**: Пользовательский интерфейс, позволяющий добавлять новых участников и просматривать список существующих. Общается с бэкендом через HTTP-запросы.

**Схема взаимодействия:**
`Streamlit (User UI) <-> FastAPI (Business Logic) <-> PostgreSQL (Data Storage)`

В Kubernetes взаимодействие настроено через DNS-имена сервисов (`backend-service`, `postgres-service`).

### 3. Технологический стек
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn.
- **Frontend**: Python, Streamlit, Pandas, Requests.
- **Database**: PostgreSQL 13.
- **Orchestration**: Docker, Kubernetes.

### 4. Листинги кода

#### Backend: `src/backend/main.py`
```python
# (Код Backend API)
# См. файл src/backend/main.py
```

#### Frontend: `src/frontend/app.py`
```python
# (Код Frontend UI)
# См. файл src/frontend/app.py
```

#### Dockerfiles
**Backend:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Kubernetes Manifest: `k8s/fullstack.yaml`
```yaml
# (Полный манифест Deployment и Service)
# См. файл k8s/fullstack.yaml
```

### 5. Скриншоты выполнения

#### Сборка образов
<img width="1375" height="629" alt="Снимок экрана 2026-03-30 145816" src="https://github.com/user-attachments/assets/8941d4e7-44cb-4433-85bf-64594eab8978" />
<img width="1380" height="358" alt="Снимок экрана 2026-03-30 151157" src="https://github.com/user-attachments/assets/6a368ec8-7169-4c9a-9f2b-12d843978827" />

#### Статус подов
<img width="688" height="98" alt="image" src="https://github.com/user-attachments/assets/ea52ec0d-3640-4cc7-9c62-1d944b4583e0" />

```bash
# kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
postgres-deploy-xxxxxxxx-xxxxx     1/1     Running   0          5m
backend-deploy-xxxxxxxx-xxxxx      1/1     Running   0          4m
frontend-deploy-xxxxxxxx-xxxxx     1/1     Running   0          4m
```

#### Работающее приложение
<img width="1851" height="979" alt="image" src="https://github.com/user-attachments/assets/ee4873a5-402f-4a01-8634-e7957c6946ce" />


База данных:
<img width="815" height="354" alt="image" src="https://github.com/user-attachments/assets/d4493722-f88f-4cca-94a1-b6eb4710fd3a" />

<img width="522" height="248" alt="image" src="https://github.com/user-attachments/assets/a9c5509a-e2b7-4538-8b30-2c527b4bbb75" />

