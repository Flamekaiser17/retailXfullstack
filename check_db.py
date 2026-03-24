import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from products.models import Product, PriceHistory

p = Product.objects.first()
if p:
    print(f'Product: {p.product_name}')

    count = PriceHistory.objects.filter(product=p).count()
    print(f'Price History Count: {count}')

    if count < 2:
        for i in range(5):
            PriceHistory.objects.get_or_create(
                product=p, 
                price=p.price - i*10
            )
        print('Sample data created!')
    else:
        print('Data already exists!')
else:
    print('No products found in database!')
