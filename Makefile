all: build down up pull_llama3 migrate run

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
	python ./django/manage.py makemigrations

migrate:
	python ./django/manage.py migrate

run:
	python ./django/manage.py runserver

super:
	python ./django/manage.py createsuperuser

proj:
	django-admin startproject $(p)

app:
	python ./django/manage.py start app $(a)

static:
	python ./django/manage.py collectstatic

edjango:
	docker exec -it ai_blog_app bash

# Ollama
pull_llama3:
	docker exec -it ollama_app bash -c "ollama pull llama3"  

eollama:
	docker exec -it ollama_app bash
