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

.PHONY: test
test:	## Run project unit tests with coverage
	docker-compose exec web-mols pytest .

.PHONY: isort
isort:  ## Sort imports in project code
	docker-compose exec web-mols isort .

.PHONY: black
black:  ## Apply black in project code
	docker-compose exec web-mols black --fast .

.PHONY: mypy
mypy:  ## Run mypy checks on project code
	docker-compose exec web-mols mypy --ignore-missing-imports .

.PHONY: flake8
flake8:  ## Flake8 checks on project code
	docker-compose exec web-mols flake8 .
