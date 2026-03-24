import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
apps = SocialApp.objects.all()
print(f"Total SocialApps: {apps.count()}")
if apps.count() > 1:
    keep = apps.first()
    apps.exclude(pk=keep.pk).delete()
    print("Duplicates deleted!")
else:
    SocialApp.objects.all().delete()
    print("All deleted - fresh start!")
