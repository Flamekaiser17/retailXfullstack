"""
products/signals.py — Auto-record price history whenever a product price changes.
This is what makes RetailX different: users can see if a price is genuinely a deal.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product, PriceHistory


@receiver(pre_save, sender=Product)
def record_price_history(sender, instance, **kwargs):
    """Auto-record price change whenever product is saved with a different price."""
    try:
        old = Product.objects.get(pk=instance.pk)
        if old.price != instance.price:
            # price changed — will record AFTER save via post_save
            instance._price_changed = True
            instance._old_price = old.price
        else:
            instance._price_changed = False
    except Product.DoesNotExist:
        # New product — record initial price after save
        instance._price_changed = True
        instance._old_price = None


@receiver(post_save, sender=Product)
def save_price_history(sender, instance, created, **kwargs):
    """Save the price history record after product save."""
    if created:
        PriceHistory.objects.create(
            product=instance,
            price=instance.price,
            note='Initial price'
        )
    elif getattr(instance, '_price_changed', False):
        PriceHistory.objects.create(
            product=instance,
            price=instance.price,
            note='Price updated'
        )
