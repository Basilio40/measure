release:  python manage.py migrate
web:  bin/start-nginx gunicorn -w $WORKERS -c gunicorn_config.py config.wsgi:application
worker: celery -A config  worker -l INFO

