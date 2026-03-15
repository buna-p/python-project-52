install:
	uv sync

collectstatic:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py migrate --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .