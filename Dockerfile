FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "task_scheduler.wsgi:application", "--bind", "0.0.0.0:8000"]

RUN chmod +x /app/entrypoint.sh
