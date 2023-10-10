pytest:
	${test_env} /bin/bash -c "pytest --cov=metisse -s -q /app/pytest_metisse/*"
.PHONY: pytest

# local-test
local-test:
	@poetry run pytest --cov=metisse -s pytest_metisse
.PHONY: local-test

# docker run
test:
	@make pytest test_env="docker compose run --rm -w /app xvfb-service" \
	server='--server=\"xvfb-service\"'
.PHONY: test

# coverage
coverage-local-test:
	@poetry run pytest --cov=metisse -s pytest_metisse
.PHONY: coverage-local-test

coverage-html:
	coverage html
.PHONY: coverage-html

coverage-xml:
	coverage xml -o cov.xml
.PHONY: coverage-xml

# docker
build:
	docker build --pull --no-cache -t weekanda7/metisse-test:latest . && \
	docker push weekanda7/metisse-test:latest
.PHONY: build

pull:
	docker pull weekanda7/metisse-test:latest
.PHONY: pull

# docker-compose
up:
	docker-compose up -d
.PHONY: up


down:
	docker-compose down
.PHONY: down

# poetry
lint:
	poetry run isort .
	poetry run black .
.PHONY: lint



install:
	poetry install
.PHONY: install

_export:
	poetry export --without-hashes --format=requirements.txt --output requirements.txt
.PHONY: _export



# 判斷操作系統
ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q .venv
else
    RM = rm -rf .venv
endif

# 定義clean-venv目標
clean-venv:
	$(RM)
.PHONY: clean-venv
