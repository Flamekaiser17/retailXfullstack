"""
WSGI config for ecomm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')

# Initialize Django
django.setup()

# EXTREMELY HELPFUL: Run migrations automatically on server startup
# This is production-safe on single-worker free plans (like Render Free)
try:
    print("🚀 Initializing Production Database...")
    call_command('migrate', interactive=False)
    print("✅ Database Migrations Applied Successfully.")
    
    # Optional: Automatically create a superuser if it doesn't exist (if create_superuser.py is present)
    if os.path.exists('create_superuser.py'):
        import subprocess
        subprocess.run(['python', 'create_superuser.py'], capture_output=True)
        print("👤 Superuser check/creation finished.")

except Exception as e:
    print(f"⚠️ Automatic Migration Failed: {e}")

# The standard WSGI application
application = get_wsgi_application()
