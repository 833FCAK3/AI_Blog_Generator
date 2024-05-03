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

# Ollama
pull_llama3:
	docker exec -it ollama_app bash -c "ollama pull llama3"  

eollama:
	docker exec -it ollama_app bash
