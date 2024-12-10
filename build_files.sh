#!/bin/bash

echo "Starting build process..."
echo "Installing requirements and collecting static files"

poetry shell
poetry config virtualenvs.in-project true
poetry install
poetry run python manage.py collectstatic --no-input


echo "Build process complete"