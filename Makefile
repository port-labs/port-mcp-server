.PHONY: lint format type-check test test-cov coverage-html clean build publish bump-version tag release install help pre-commit all

# Default target executed when no arguments are given to make.
all: help

POETRY_CHECK := $(shell command -v poetry 2> /dev/null)
POETRY := poetry
RUN_CMD := poetry run
PYTHON := python

help:
	@echo "Available commands:"
	@echo "  make lint         : Run all linting checks (Ruff, mypy)"
	@echo "  make format       : Format code with Ruff"
	@echo "  make type-check   : Run mypy for type checking"
	@echo "  make pre-commit   : Run all pre-commit hooks"
	@echo "  make test         : Run tests"
	@echo "  make test-cov     : Run tests with coverage report in terminal"
	@echo "  make coverage-html: Generate HTML coverage report"
	@echo "  make clean        : Remove build artifacts"
	@echo "  make install      : Install dependencies"
	@echo "  make build        : Build package"
	@echo "  make publish      : Publish package to PyPI"
	@echo "  make bump-version : Bump version (use VERSION=X.Y.Z)"
	@echo "  make release      : Full release process"

lint:
	@echo "Running linting checks..."
	$(RUN_CMD) ruff check src
	$(RUN_CMD) mypy server

format:
	@echo "Formatting code..."
	$(RUN_CMD) ruff format src

type-check:
	@echo "Running type checks..."
	$(RUN_CMD) mypy src

pre-commit:
	@echo "Running pre-commit hooks..."
	$(PYTHON) -m pre-commit run --all-files

test:
	@echo "Running tests..."
	export PORT_CLIENT_ID=1234567890
	export PORT_CLIENT_SECRET=1234567890
	export PORT_REGION=EU
	export PORT_LOG_LEVEL=DEBUG
	$(PYTHON) -m pytest tests/ -v
	unset PORT_CLIENT_ID
	unset PORT_CLIENT_SECRET
	unset PORT_REGION
	unset PORT_LOG_LEVEL

test-cov:
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest --cov=src --cov-report=term-missing --cov-branch

coverage-html:
	@echo "Generating HTML coverage report..."
	$(PYTHON) -m pytest --cov=src --cov-report=html --cov-branch
	@echo "HTML report generated in htmlcov/ directory"

clean:
	@echo "Cleaning up..."
	rm -rf dist/ build/ *.egg-info/ .coverage coverage.xml htmlcov/ .pytest_cache/ .ruff_cache/ .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

install:
	@echo "Installing dependencies..."
	if [ -z "$(POETRY_CHECK)" ]; then \
		$(PYTHON) -m pip install poetry 2> /dev/null 1> /dev/null; \
	fi
	$(POETRY) install
	
bump-version:
ifndef VERSION
	$(error VERSION is not set. Use 'make bump-version VERSION=X.Y.Z')
endif
	sed -i '' 's/version = "[^"]*"/version = "$(VERSION)"/' pyproject.toml

tag:
ifndef VERSION
	$(error VERSION is not set. Use 'make tag VERSION=X.Y.Z')
endif
	git add pyproject.toml
	git commit -m "chore: bump version to $(VERSION)"
	git push origin main
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin v$(VERSION)

build: clean
	$(PYTHON) -m pip install --upgrade build twine
	$(PYTHON) -m build

publish:
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload dist/*

release: bump-version tag build publish 