PACKAGES := pydantic_requests tests

hash := $(word 1, $(shell grep -i  content-hash poetry.lock | shasum))

.PHONY: all
all: install

.PHONY: install
install: .venv/$(hash)
.venv/$(hash):
	mkdir .venv
	poetry install
	@ touch $@

.PHONY: fmt
fmt: install
	poetry run autoflake --remove-all-unused-imports -i -r $(PACKAGES)
	poetry run black $(PACKAGES)
	poetry run isort $(PACKAGES) --recursive --apply

.PHONY: release
release: install
	poetry build
	poetry publish

.PHONY: lint
lint: install
	poetry run isort $(PACKAGES) --recursive --check-only --diff
	poetry run mypy pydantic_requests

.PHONY: unit
unit:test
.PHONY: test
test: install
	@find . -name "__pycache__" -type d | xargs rm -rf
	poetry run pytest --cov=pydantic_requests

.PHONY: watch
watch: install
	poetry run rerun "make test format check" -i .coverage -i htmlcov

.PHONY: clean
clean:
	rm -rf .venv
