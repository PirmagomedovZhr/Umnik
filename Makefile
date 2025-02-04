local_up:
	docker-compose build
	chmod -R 777 ./media/
	docker-compose up -d

local_down:
	docker-compose down

test:
	docker-compose run --rm web sh -c "python manage.py test"

makemigrations:
	docker-compose run --rm web sh -c "python manage.py makemigrations"

migrate:
	docker-compose run --rm web sh -c "python manage.py migrate"

createsuperuser:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"

dbshell:
	docker-compose exec db psql -U postgres -d postgres
