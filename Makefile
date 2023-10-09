# local-test
test:
	@poetry run pytest -s pytest_metisse
.PHONY: test


# docker
build:
	docker build --pull --no-cache -t weekanda7/metisse-test:latest . && \
	docker push weekanda7/metisse-test:latest
.PHONY: build


pull:
	docker pull weekanda7/metisse-test:latest
.PHONY: pull


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

clean-venv:
	rm -rf .venv
.PHONY: clean-venv

