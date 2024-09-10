#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
echo "Installing dependencies..."
pip install -r requirements.txt

# Convert static asset files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
echo "Applying database makemigrations..."
python manage.py makemigrations
python manage.py migrate auth
python manage.py migrate
echo "Applying database migrations..."
python manage.py migrate
