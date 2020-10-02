web: gunicorn config.wsgi:application
worker: celery worker --app=techfest.taskapp --loglevel=info
