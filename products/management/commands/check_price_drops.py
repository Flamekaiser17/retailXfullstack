from django.core.management.base import BaseCommand
from products.models import PriceAlert
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Check all active price alerts and send emails if the target price is reached'

    def handle(self, *args, **kwargs):
        active_alerts = PriceAlert.objects.filter(is_active=True)
        emails_sent = 0
        
        self.stdout.write(self.style.NOTICE(f"Checking {active_alerts.count()} active price alerts..."))
        
        for alert in active_alerts:
            # The alert activates if current product price is <= target price
            if alert.product.price <= alert.target_price:
                subject = f"Price Drop Alert: {alert.product.product_name}!"
                message = f"Good news {alert.user.first_name}!\n\nThe price for {alert.product.product_name} has dropped to ₹{alert.product.price}, which is at or below your target of ₹{alert.target_price}.\n\nGrab it now before it goes out of stock!\n\nRegards,\nRetailX Team"
                
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [alert.user.email],
                        fail_silently=False  # Good for debugging if SMTP isn't set up perfectly yet
                    )
                    # Deactivate alert after sending the notification so we don't spam
                    alert.is_active = False
                    alert.save()
                    emails_sent += 1
                    self.stdout.write(self.style.SUCCESS(f"Sent price drop alert to {alert.user.email} for {alert.product.product_name} (₹{alert.product.price})"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to send email to {alert.user.email}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Job complete. Sent {emails_sent} price drop emails."))
