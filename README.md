# nrsak-py

[![CI](https://github.com/23skdu/nrsak-py/actions/workflows/ci.yml/badge.svg)](https://github.com/23skdu/nrsak-py/actions/workflows/ci.yml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/23skdu/nrsak-py/network/updates)

A small Python "Swiss Army Knife" for the New Relic REST and NerdGraph APIs.

## Build

```bash
docker build -t nrsak-py:latest .
```

## Run

```bash
docker run --rm -e NR_KEY=XXXXXXXXXXXXXX nrsak-py:latest function_list
docker run --rm -e NR_KEY=XXXXXXXXXXXXXX nrsak-py:latest nrSummary
```

Pipe the JSON output to `jq`:

```bash
docker run --rm -e NR_KEY=XXXXXXXXXXXXXX nrsak-py:latest nrSummary | jq '.applications[].name'
```

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

See [docs/cli.md](docs/cli.md) for the full CLI reference.
