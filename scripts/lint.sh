#!/usr/bin/env bash

set -x
set -e

poetry run mypy src
poetry run black src tests
poetry run isort src tests
poetry run flake8 src tests