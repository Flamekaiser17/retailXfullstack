"""
Script to populate the database with sample products across multiple categories.
Categories: Men's Fashion, Women's Fashion, Electronics, Home & Kitchen, Sports & Outdoor
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from products.models import Category, Product, ProductImage, SizeVariant, ColorVariant

# Create categories
categories_data = [
    {"name": "Men's Fashion", "image": "https://images.unsplash.com/photo-1490114538077-0a7f8cb49891?w=500"},
    {"name": "Women's Fashion", "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=500"},
    {"name": "Electronics", "image": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500"},
    {"name": "Home & Kitchen", "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500"},
    {"name": "Sports & Outdoor", "image": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500"},
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        category_name=cat_data["name"],
        defaults={"category_image": cat_data["image"]}
    )
    if created:
        print(f"✓ Created category: {cat_data['name']}")
    else:
        print(f"- Category already exists: {cat_data['name']}")

# Create size variants
sizes_data = [
    {"name": "XS", "price": 0, "order": 1},
    {"name": "S", "price": 0, "order": 2},
    {"name": "M", "price": 0, "order": 3},
    {"name": "L", "price": 50, "order": 4},
    {"name": "XL", "price": 100, "order": 5},
    {"name": "XXL", "price": 150, "order": 6},
]

print("\nCreating size variants...")
for size_data in sizes_data:
    size, created = SizeVariant.objects.get_or_create(
        size_name=size_data["name"],
        defaults={"price": size_data["price"], "order": size_data["order"]}
    )
    if created:
        print(f"✓ Created size: {size_data['name']}")

# Products data
products_data = [
    # Men's Fashion
    {
        "name": "Classic Denim Jacket",
        "category": "Men's Fashion",
        "price": 2499,
        "description": "Timeless denim jacket with a modern fit. Perfect for casual outings and layering. Made from premium quality denim fabric.",
        "images": [
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",
            "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500"
        ],
        "newest": True
    },
    {
        "name": "Slim Fit Chinos",
        "category": "Men's Fashion",
        "price": 1899,
        "description": "Comfortable slim fit chinos available in multiple colors. Perfect for both office and casual wear.",
        "images": ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500"],
        "newest": False
    },
    {
        "name": "Cotton Polo T-Shirt",
        "category": "Men's Fashion",
        "price": 899,
        "description": "Premium cotton polo t-shirt with breathable fabric. Available in various colors and sizes.",
        "images": ["https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"],
        "newest": True
    },
    
    # Women's Fashion
    {
        "name": "Floral Summer Dress",
        "category": "Women's Fashion",
        "price": 2199,
        "description": "Beautiful floral print summer dress with comfortable fit. Perfect for parties and casual outings.",
        "images": [
            "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500",
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500"
        ],
        "newest": True
    },
    {
        "name": "Designer Handbag",
        "category": "Women's Fashion",
        "price": 3499,
        "description": "Elegant designer handbag with premium leather finish. Multiple compartments for organized storage.",
        "images": ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500"],
        "newest": False
    },
    {
        "name": "Casual Sneakers",
        "category": "Women's Fashion",
        "price": 1599,
        "description": "Comfortable casual sneakers perfect for everyday wear. Lightweight and stylish design.",
        "images": ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"],
        "newest": True
    },
    
    # Electronics
    {
        "name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "price": 4999,
        "description": "Premium wireless headphones with active noise cancellation. 30-hour battery life and superior sound quality.",
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500"
        ],
        "newest": True
    },
    {
        "name": "Smart Watch Pro",
        "category": "Electronics",
        "price": 8999,
        "description": "Advanced smartwatch with fitness tracking, heart rate monitor, and GPS. Water-resistant design.",
        "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"],
        "newest": True
    },
    {
        "name": "Portable Power Bank 20000mAh",
        "category": "Electronics",
        "price": 1799,
        "description": "High-capacity power bank with fast charging support. Charge multiple devices simultaneously.",
        "images": ["https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500"],
        "newest": False
    },
    {
        "name": "4K Action Camera",
        "category": "Electronics",
        "price": 12999,
        "description": "Professional 4K action camera with waterproof housing. Perfect for adventure and sports photography.",
        "images": ["https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500"],
        "newest": True
    },
    
    # Home & Kitchen
    {
        "name": "Stainless Steel Cookware Set",
        "category": "Home & Kitchen",
        "price": 5499,
        "description": "Premium 7-piece stainless steel cookware set. Includes pots, pans, and lids. Dishwasher safe.",
        "images": ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"],
        "newest": False
    },
    {
        "name": "Electric Kettle 1.7L",
        "category": "Home & Kitchen",
        "price": 1299,
        "description": "Fast-boiling electric kettle with auto shut-off feature. Stainless steel body with LED indicator.",
        "images": ["https://images.unsplash.com/photo-1563822249366-7efbeb0d7e46?w=500"],
        "newest": True
    },
    {
        "name": "Non-Stick Frying Pan",
        "category": "Home & Kitchen",
        "price": 899,
        "description": "Durable non-stick frying pan with ergonomic handle. Suitable for all cooktops including induction.",
        "images": ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"],
        "newest": False
    },
    {
        "name": "Ceramic Dinner Set 24 Pieces",
        "category": "Home & Kitchen",
        "price": 3999,
        "description": "Elegant ceramic dinner set for 6 people. Microwave and dishwasher safe. Modern design.",
        "images": ["https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=500"],
        "newest": True
    },
    
    # Sports & Outdoor
    {
        "name": "Yoga Mat Premium",
        "category": "Sports & Outdoor",
        "price": 1499,
        "description": "Extra thick yoga mat with non-slip surface. Eco-friendly material with carrying strap included.",
        "images": ["https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"],
        "newest": True
    },
    {
        "name": "Adjustable Dumbbells Set",
        "category": "Sports & Outdoor",
        "price": 4999,
        "description": "Adjustable dumbbell set 5-25kg. Space-saving design perfect for home gym. Includes storage tray.",
        "images": ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"],
        "newest": False
    },
    {
        "name": "Camping Tent 4-Person",
        "category": "Sports & Outdoor",
        "price": 6999,
        "description": "Waterproof camping tent for 4 people. Easy setup with UV protection and ventilation windows.",
        "images": ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"],
        "newest": True
    },
    {
        "name": "Mountain Bike 21-Speed",
        "category": "Sports & Outdoor",
        "price": 18999,
        "description": "Durable mountain bike with 21-speed gear system. Front suspension and disc brakes for safety.",
        "images": ["https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500"],
        "newest": True
    },
]

print("\nCreating products...")
for prod_data in products_data:
    category = Category.objects.get(category_name=prod_data["category"])
    
    product, created = Product.objects.get_or_create(
        product_name=prod_data["name"],
        defaults={
            "category": category,
            "price": prod_data["price"],
            "product_desription": prod_data["description"],
            "newest_product": prod_data["newest"]
        }
    )
    
    if created:
        print(f"✓ Created product: {prod_data['name']}")
        
        # Add product images
        for img_url in prod_data["images"]:
            ProductImage.objects.create(
                product=product,
                image_url=img_url
            )
        print(f"  - Added {len(prod_data['images'])} image(s)")
    else:
        print(f"- Product already exists: {prod_data['name']}")

print("\n" + "="*50)
print("Database population complete!")
print("="*50)
print(f"Total categories: {Category.objects.count()}")
print(f"Total products: {Product.objects.count()}")
print(f"Total product images: {ProductImage.objects.count()}")
