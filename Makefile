.PHONY: install run stop quality style

check_dirs := backend frontend

install:
	pip install -e ".[quality]"

run:
	docker-compose up --build

stop:
	docker-compose down

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black $(check_dirs)
	isort $(check_dirs)
