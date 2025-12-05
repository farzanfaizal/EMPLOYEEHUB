#!/usr/bin/env bash
# Professional Render Build Script
# Exit on error
set -o errexit

echo "🚀 Starting EmployeeHub build process..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories (BEFORE Django runs)
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p media
mkdir -p media/profile_pictures
mkdir -p staticfiles

echo "✅ Directories created successfully"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input

# Create Django Site (required for allauth)
echo "🌐 Configuring Django Site..."
python manage.py shell <<EOF
from django.contrib.sites.models import Site
try:
    site = Site.objects.get(id=1)
    if 'render.com' in '$RENDER_EXTERNAL_URL':
        domain = '$RENDER_EXTERNAL_URL'.replace('https://', '').replace('http://', '')
        site.domain = domain
        site.name = 'EmployeeHub'
        site.save()
        print(f'✅ Site configured: {domain}')
    else:
        print('⚠️  RENDER_EXTERNAL_URL not set, using default site config')
except Exception as e:
    print(f'⚠️  Site configuration skipped: {e}')
EOF

echo "✅ Build completed successfully!"
echo "🎉 EmployeeHub is ready to deploy!"
