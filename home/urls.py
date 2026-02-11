from django.urls import path
from home.views import *
from home.health import health_check

urlpatterns = [
    path('', index, name="index"),
    path('health/', health_check, name='health_check'),
    path('search/', product_search, name='product_search'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
]
