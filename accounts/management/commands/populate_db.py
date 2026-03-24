from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **kwargs):
        # Check if products already exist
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Products already exist. Skipping...'))
            return

        # Create categories
        categories_data = [
            'Electronics',
            'Fashion',
            'Home & Kitchen',
            'Books',
            'Sports',
        ]

        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(
                category_name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories[cat_name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Create sample products
        products_data = [
            {
                'name': 'Wireless Headphones',
                'price': 2999,
                'category': 'Electronics',
                'description': 'High-quality wireless headphones with noise cancellation',
                'image': 'https://source.unsplash.com/800x600/?headphones',
            },
            {
                'name': 'Smart Watch',
                'price': 4999,
                'category': 'Electronics',
                'description': 'Feature-rich smartwatch with fitness tracking',
                'image': 'https://source.unsplash.com/800x600/?smartwatch',
            },
            {
                'name': 'Cotton T-Shirt',
                'price': 499,
                'category': 'Fashion',
                'description': 'Comfortable cotton t-shirt for everyday wear',
                'image': 'https://source.unsplash.com/800x600/?tshirt',
            },
            {
                'name': 'Denim Jeans',
                'price': 1299,
                'category': 'Fashion',
                'description': 'Classic denim jeans with perfect fit',
                'image': 'https://source.unsplash.com/800x600/?jeans',
            },
            {
                'name': 'Coffee Maker',
                'price': 3499,
                'category': 'Home & Kitchen',
                'description': 'Automatic coffee maker for perfect brew',
                'image': 'https://source.unsplash.com/800x600/?coffee-maker',
            },
            {
                'name': 'Cooking Pan Set',
                'price': 1999,
                'category': 'Home & Kitchen',
                'description': 'Non-stick cooking pan set of 3',
                'image': 'https://source.unsplash.com/800x600/?cookware',
            },
            {
                'name': 'Python Programming Book',
                'price': 599,
                'category': 'Books',
                'description': 'Learn Python programming from scratch',
                'image': 'https://source.unsplash.com/800x600/?book',
            },
            {
                'name': 'Yoga Mat',
                'price': 799,
                'category': 'Sports',
                'description': 'Premium yoga mat with anti-slip surface',
                'image': 'https://source.unsplash.com/800x600/?yoga',
            },
            {
                'name': 'Running Shoes',
                'price': 2499,
                'category': 'Sports',
                'description': 'Comfortable running shoes for athletes',
                'image': 'https://source.unsplash.com/800x600/?running-shoes',
            },
            {
                'name': 'Laptop Backpack',
                'price': 1499,
                'category': 'Electronics',
                'description': 'Spacious backpack for laptop and accessories',
                'image': 'https://source.unsplash.com/800x600/?backpack',
            },
        ]

        for product_data in products_data:
            category = categories[product_data['category']]
            product = Product.objects.create(
                product_name=product_data['name'],
                slug=slugify(product_data['name']),
                price=product_data['price'],
                category=category,
                product_desription=product_data['description'], # Fixed typo mismatch
                newest_product=True,
            )
            # Correctly handle images via ProductImage model
            ProductImage.objects.create(
                product=product,
                image_url=product_data['image']
            )
            self.stdout.write(self.style.SUCCESS(f'Created product: {product_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(products_data)} products!'))
