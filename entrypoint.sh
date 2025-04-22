echo "در حال اعمال مایگریشن‌ها..."
python manage.py migrate

echo "در حال جمع‌آوری فایل‌های استاتیک..."
python manage.py collectstatic --noinput

echo "شروع سرور Django..."
gunicorn task_scheduler.wsgi:application --bind 0.0.0.0:8000
