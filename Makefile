all: build down migrate_c pull_llama3 up

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

migrate_c:
	docker-compose run ai_blog_app bash -c "python manage.py migrate"

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

edjango:
	docker exec -it ai_blog_app bash

# Ollama
pull_llama3:
	docker exec -it ollama_app bash -c "ollama pull llama3"  

eollama:
	docker exec -it ollama_app bash
