#!/bin/bash
echo "Starting build process..."
echo "Installing requirements and collecting static files"
pip install -r requirements.txt
python manage.py collectstatic --no-input
echo "Build process complete"