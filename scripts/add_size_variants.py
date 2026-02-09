import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from products.models import Product, SizeVariant, ProductImage
import random

print("🔧 Adding size variants to fashion products...")
print("=" * 60)

# Get all size variants
sizes = SizeVariant.objects.all()
print(f"✅ Found {sizes.count()} size variants: {[s.size_name for s in sizes]}")

# Get fashion categories
fashion_categories = ['Men\'s Fashion', 'Women\'s Fashion']

for category_name in fashion_categories:
    print(f"\n📦 Processing {category_name}...")
    products = Product.objects.filter(category__category_name=category_name)
    print(f"   Found {products.count()} products")
    
    for product in products:
        # Check if product already has sizes
        if product.size_variant.count() == 0:
            # Add random 4-6 sizes to each product
            num_sizes = random.randint(4, 6)
            selected_sizes = random.sample(list(sizes), min(num_sizes, sizes.count()))
            product.size_variant.set(selected_sizes)
            print(f"   ✅ Added {len(selected_sizes)} sizes to: {product.product_name}")
        else:
            print(f"   ⏭️  Skipped (already has sizes): {product.product_name}")

print("\n" + "=" * 60)
print("✅ Size variants added successfully!")
print("\n📊 Summary:")

# Print summary
for category_name in fashion_categories:
    products = Product.objects.filter(category__category_name=category_name)
    total = products.count()
    with_sizes = sum(1 for p in products if p.size_variant.count() > 0)
    print(f"   {category_name}: {with_sizes}/{total} products have sizes")
