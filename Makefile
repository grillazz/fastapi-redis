.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build project with compose
	docker-compose build

.PHONY: up
up:	## Run project with compose
	docker-compose up

.PHONY: down
down: ## Stop project containers with compose
	docker-compose down

.PHONY: clean
clean: ## Reset project containers with compose
	docker-compose down -v --remove-orphans

.PHONY: lock
lock:	## Refresh pipfile.lock
	pipenv lock --pre

.PHONY: requirements
requirements:	## Refresh requirements.txt from pipfile.lock
	pipenv lock -r > requirements.txt

.PHONY: test-cov
test-cov:	## Run project unit tests with coverage
	docker-compose exec web pytest . -vv

.PHONY: isort
isort:  ## sort imports in project code
	docker-compose exec web isort .

.PHONY: black
black:  ## apply black in project code
	docker-compose exec web black --fast .

.PHONY: mypy
mypy:  ## run flake8 checks on project code
	docker-compose exec web mypy --ignore-missing-imports .

.PHONY: flake8
flake8:  ## run flake8 checks on project code
	docker-compose exec web flake8 .