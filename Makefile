install:
	pip install -r requirements.txt

run:
	python manage.py runserver "0.0.0.0:8099"

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	python manage.py test

shell:
	python manage.py shell

dbshell:
	python manage.py dbshell

backup:
	python manage.py dumpdata > db_backup.json

createadmin:
	python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@admin.com').exists() or User.objects.create_superuser('admin@admin.com', 'admin@admin.com', 'admin')"

reset:
	find */migrations -name "*.pyc" -delete
	find */migrations -name "*.py" -not -name "__init__.py" -delete
	rm -rf db.sqlite3

createadmin2:
	python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='root@root.com').exists() or User.objects.create_superuser('root@root.com', 'root@root.com', 'root')"

locale:
	django-admin makemessages -l pt_BR --ignore=env/*
