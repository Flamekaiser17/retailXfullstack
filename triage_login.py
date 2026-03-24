import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from django.test import RequestFactory
from accounts.views import login_page
from django.db.models import Q

rf = RequestFactory()
request = rf.get('/accounts/login/')

try:
    response = login_page(request)
    print(f'Success: {response.status_code}')
except Exception as e:
    import traceback
    print(f'Error: {e}')
    traceback.print_exc()
