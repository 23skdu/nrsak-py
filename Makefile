# Makefile for nrsak-py
.RECIPEPREFIX := >
PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

.PHONY: help venv install lint format typecheck security static test clean

help:
> @echo "Targets:"
> @echo "  venv      - create virtual environment if missing"
> @echo "  install   - install (dev) dependencies into venv"
> @echo "  lint      - run ruff lint + format check"
> @echo "  format    - apply ruff formatting"
> @echo "  typecheck - run mypy"
> @echo "  security  - run bandit"
> @echo "  static    - run all static analysis"
> @echo "  test      - run pytest"
> @echo "  clean     - remove venv and caches"

venv:
> @if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi

install: venv
> $(VENV_PIP) install --upgrade pip
> $(VENV_PIP) install -r requirements-dev.txt

lint: install
> $(VENV)/bin/ruff check .
> $(VENV)/bin/ruff format --check .

format: install
> $(VENV)/bin/ruff format .

typecheck: install
> $(VENV)/bin/mypy nrsak.py

security: install
> $(VENV)/bin/bandit -r nrsak.py

static: lint typecheck security

test: install
> $(VENV_PYTHON) -m pytest

clean:
> rm -rf $(VENV)
> rm -rf .pytest_cache .mypy_cache .ruff_cache
> find . -type d -name __pycache__ -prune -exec rm -rf {} +
> find . -type f -name '*.pyc' -delete
