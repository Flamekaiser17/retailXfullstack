import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from products.models import Product, ProductImage
import random

print("🖼️  Adding multiple images to products...")
print("=" * 60)

# Sample Unsplash image URLs for different categories
image_templates = {
    "Men's Fashion": [
        "https://images.unsplash.com/photo-1490114538077-0a7f8cb49891?w=500",
        "https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?w=500",
        "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500",
        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500",
    ],
    "Women's Fashion": [
        "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=500",
        "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=500",
        "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500",
        "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500",
    ],
    "Electronics": [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500",
        "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500",
        "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500",
    ],
    "Home & Kitchen": [
        "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500",
        "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500",
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500",
    ],
    "Sports & Outdoor": [
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500",
        "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=500",
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500",
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500",
    ],
}

# Process each category
for category_name, image_urls in image_templates.items():
    print(f"\n📦 Processing {category_name}...")
    products = Product.objects.filter(category__category_name=category_name)[:10]  # First 10 products
    
    for product in products:
        current_images = product.product_images.count()
        
        if current_images < 3:
            # Add 2-3 more images
            images_to_add = min(3 - current_images, len(image_urls))
            selected_images = random.sample(image_urls, images_to_add)
            
            for img_url in selected_images:
                ProductImage.objects.create(product=product, image_url=img_url)
            
            print(f"   ✅ Added {images_to_add} images to: {product.product_name} (now has {current_images + images_to_add})")
        else:
            print(f"   ⏭️  Skipped: {product.product_name} (already has {current_images} images)")

print("\n" + "=" * 60)
print("✅ Multiple images added successfully!")
