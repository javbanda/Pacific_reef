web: cd DjangoReef && pip install --no-cache-dir -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn PacificReef.wsgi --bind 0.0.0.0:$PORT
