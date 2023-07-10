lint:
	poetry run flake8 page_analyzer

install:
	poetry install

PORT ?= 8000
start:
	gunicorn task_manager.wsgi
