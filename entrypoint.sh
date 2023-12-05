#!/bin/bash
set -e

# Apply Django migrations
python ivrMock/manage.py migrate

#python ivrMock/manage.py createsuperuser --noinput --username $DJANGO_USER --email $DJANGO_EMAIL
#python ivrMock/manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='$DJANGO_USER'); u.set_password('$DJANGO_PASSWORD'); u.save()"

cd ivrMock
celery -A ivrMock worker --loglevel=info &
# celery -A app worker -l info
cd ..

# Start the Django server on port 7000
python ivrMock/manage.py runserver 0.0.0.0:7000
