#!/usr/bin/env python
"""
Auto-create superuser if none exists
Run this after migrations in build.sh
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if any superuser exists
if not User.objects.filter(is_superuser=True).exists():
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@retailx.com',
        password='admin123'  # Change this after first login!
    )
    # Ensure profile is verified for immediate login
    user.profile.is_email_verified = True
    user.profile.save()
    print("✅ Superuser created: username='admin', password='admin123'")
    print("⚠️  IMPORTANT: Change password after first login!")
else:
    print("ℹ️  Superuser already exists, skipping creation")
