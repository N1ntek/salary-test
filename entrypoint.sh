#!/bin/sh
set -e

echo "Run alembic migrations..."
poetry run alembic upgrade head

echo "App start..."
poetry run python main.py