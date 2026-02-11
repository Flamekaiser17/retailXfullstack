#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser automatically
python create_superuser.py

# Populate database with sample products
python manage.py populate_db

echo "Build completed successfully!"
