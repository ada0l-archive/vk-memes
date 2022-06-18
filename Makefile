CODE = backend
SRC = .

run: init_db
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 4

generate: init_db
	poetry run python -m schedule_generator.main

init_db:
	poetry run alembic upgrade head