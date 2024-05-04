.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: django-migrate
django-migrate: ## apply migrations
	cd 02_movies_admin && ./manage.py migrate --fake --fake movies 0001 && ./manage.py migrate

.PHONY: django-makemigrations
django-makemigrations: ## apply migrations
	cd 02_movies_admin && ./manage.py makemigrations

.PHONY: start-app
start-app: ## start dev server
	cd 02_movies_admin && ./manage.py runserver

.PHONY: admin
admin: ## create admin user
	cd 02_movies_admin && \
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true


.PHONY: make-trans
make-trans: ## make translations
	cd 02_movies_admin && django-admin makemessages -l ru -e py -e html -i venv

.PHONY: compile-trans
compile-trans: ## compile translations
	cd 02_movies_admin && django-admin compilemessages --exclude venv

.PHONY: start-db
start-db: ## start postgres
	docker compose up -d

.PHONY: stop-db-clear
stop-db-clear: ## stop postgres and clear all
	docker compose down -v


.PHONY: transfer-data
transfer-data: ## transfer data from sqlite
	cd 03_sqlite_to_postgres && python load_data.py

.PHONY: wait_to_db
wait_to_db:
	bash -c "until docker exec theatre-db pg_isready ; do echo 'db is starting...' ; sleep 1 ; echo 'db is up' ; done"

.PHONY: install-pip
install-pip: ## install requirements
	pip install -r requirements.txt

start-all: install-pip start-db wait_to_db transfer-data django-migrate admin start-app