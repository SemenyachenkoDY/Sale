FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -u 1000 -m appuser
USER appuser

COPY app.py .

CMD ["python", "app.py"]
