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
	docker-compose exec chem-molecules pytest .

.PHONY: py-upgrade
py-upgrade:	## Upgrade project py files with pyupgrade library for python version 3.9
	docker-compose run --rm chem-molecules pyupgrade --py39-plus `find . -name "*.py"`

.PHONY: safety
safety:	## Check project and dependencies with safety https://github.com/pyupio/safety
	docker-compose run --rm chem-molecules safety check

.PHONY: lint
lint:  ## Lint project code.
	isort app tests --check
	flake8 --config .flake8 app tests
	mypy the_app tests
	black app tests --line-length=120 --check --diff

.PHONY: format
format:  ## Format project code.
	isort app tests
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app tests --exclude=__init__.py
	black app tests --line-length=120
