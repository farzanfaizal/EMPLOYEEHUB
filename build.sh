#!/usr/bin/env bash
# Render build script
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Creating migration files..."
python manage.py makemigrations --no-input

echo "🗄️  Running migrations..."
python manage.py migrate --no-input

echo "🌱 Setting up sample data..."
python manage.py setup_production

echo "✅ Build complete!"
