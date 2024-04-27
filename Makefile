all: build down up

# Docker
build:
	docker-compose build --no-cache

down:
	docker-compose down

up:
	docker-compose up -d

upp:
	docker-compose up

stop:
	docker-compose stop

clnimg:
	docker image prune -f

# Django
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver	

super:
	python manage.py createsuperuser

proj:
	django-admin startproject $(p)

app:
	python manage.py start app $(a)

static:
	python manage.py collectstatic
