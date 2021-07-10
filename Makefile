.PHONY: install clean build deploy quality style

check_dirs := backend frontend

install:
	pip install -e ".[quality]"
	pip install python-dotenv

clean:
	rm -rf deploy || true
	mkdir deploy

build:
	docker-compose build
	docker-compose push

deploy: clean build
	dotenv -f .env run kompose convert -o deploy
	kubectl apply -f deploy --namespace kompose-example

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black $(check_dirs)
	isort $(check_dirs)
