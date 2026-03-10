install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .