# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# deps Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código (em prod copie; em dev o compose monta volume por cima)
COPY app ./app

EXPOSE 8501

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
