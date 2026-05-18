up-b-d:
	docker compose up --build -d

up-b:
	docker compose up --build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f api

shell:
	docker compose exec api bash

# Migraciones
migrate:
	docker compose exec api alembic upgrade head

migration:
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

downgrade:
	docker compose exec api alembic downgrade -1
	
seed:
	docker compose exec api python seed.py
