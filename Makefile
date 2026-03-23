install:
	uv sync

collectstatic:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py migrate --noinput

dev:
	python3 manage.py runserver

tests:
	uv run ruff check .
	python3 manage.py test

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .