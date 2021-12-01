makemigrations:
	docker-compose run --rm --no-deps admin python manage.py makemigrations todo

migrate:
	docker-compose run --rm --no-deps admin python manage.py migrate

populate_local_db:
	docker-compose rm -sf db
	docker-compose up -d db
	docker-compose run --rm admin python manage.py populate_local_db