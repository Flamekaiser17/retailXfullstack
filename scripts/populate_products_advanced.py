"""
Advanced Product Database Population Script
Generates 200+ products with variants across all categories
"""

import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from products.models import Category, Product, ProductImage, SizeVariant, ColorVariant

# Color variants data
colors_data = [
    {"name": "Black", "price": 0},
    {"name": "White", "price": 0},
    {"name": "Red", "price": 100},
    {"name": "Blue", "price": 100},
    {"name": "Green", "price": 100},
    {"name": "Navy", "price": 50},
    {"name": "Grey", "price": 0},
    {"name": "Beige", "price": 50},
    {"name": "Brown", "price": 50},
    {"name": "Pink", "price": 100},
    {"name": "Yellow", "price": 100},
    {"name": "Purple", "price": 100},
    {"name": "Orange", "price": 100},
    {"name": "Maroon", "price": 50},
    {"name": "Olive", "price": 50},
]

print("="*60)
print("ADVANCED PRODUCT DATABASE POPULATION")
print("="*60)

# Create color variants
print("\n[1/4] Creating color variants...")
color_objects = []
for color_data in colors_data:
    color, created = ColorVariant.objects.get_or_create(
        color_name=color_data["name"],
        defaults={"price": color_data["price"]}
    )
    color_objects.append(color)
    if created:
        print(f"  ✓ {color_data['name']}")

# Ensure size variants exist
print("\n[2/4] Verifying size variants...")
size_names = ["XS", "S", "M", "L", "XL", "XXL"]
for size_name in size_names:
    SizeVariant.objects.get_or_create(size_name=size_name)
print(f"  ✓ {len(size_names)} sizes ready")

# Product templates by category
print("\n[3/4] Generating product data...")

products_templates = {
    "Men's Fashion": [
        # Shirts & Tops (15 products)
        ("Classic Oxford Shirt", 1499, "Premium cotton oxford shirt with button-down collar. Perfect for office and casual wear.", ["https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"]),
        ("Linen Casual Shirt", 1299, "Breathable linen shirt for summer. Lightweight and comfortable.", ["https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"]),
        ("Denim Shirt", 1799, "Classic denim shirt with chest pockets. Versatile and durable.", ["https://images.unsplash.com/photo-1603252109303-2751441dd157?w=500"]),
        ("Flannel Checkered Shirt", 1599, "Warm flannel shirt with classic check pattern.", ["https://images.unsplash.com/photo-1602810316693-3667c854239a?w=500"]),
        ("Polo T-Shirt Premium", 999, "Premium cotton polo with ribbed collar and cuffs.", ["https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"]),
        ("V-Neck T-Shirt Pack", 799, "Comfortable v-neck t-shirts. Pack of 3.", ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500"]),
        ("Henley Long Sleeve", 1199, "Classic henley with button placket. Perfect for layering.", ["https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=500"]),
        ("Graphic Print Tee", 699, "Trendy graphic print t-shirt. 100% cotton.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Striped Casual Shirt", 1399, "Horizontal striped shirt for casual outings.", ["https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500"]),
        ("Formal White Shirt", 1699, "Crisp white formal shirt. Wrinkle-free fabric.", ["https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500"]),
        ("Muscle Fit T-Shirt", 899, "Athletic fit t-shirt. Moisture-wicking fabric.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Mandarin Collar Shirt", 1499, "Modern mandarin collar shirt. Slim fit.", ["https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500"]),
        ("Rugby Polo Shirt", 1299, "Classic rugby polo with contrasting stripes.", ["https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"]),
        ("Chambray Shirt", 1599, "Lightweight chambray shirt. Perfect for layering.", ["https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"]),
        ("Printed Casual Shirt", 1399, "Vibrant printed shirt for parties and events.", ["https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500"]),
        
        # Pants & Jeans (12 products)
        ("Slim Fit Jeans", 2199, "Classic slim fit jeans with stretch. Comfortable all-day wear.", ["https://images.unsplash.com/photo-1542272604-787c3835535d?w=500", "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500"]),
        ("Chino Pants Beige", 1899, "Versatile chino pants. Perfect for office and casual.", ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500"]),
        ("Cargo Pants Olive", 1999, "Utility cargo pants with multiple pockets.", ["https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=500"]),
        ("Formal Trousers", 2299, "Wrinkle-free formal trousers. Slim fit.", ["https://images.unsplash.com/photo-1594633313593-bab3825d0caf?w=500"]),
        ("Jogger Pants", 1599, "Comfortable jogger pants with elastic waist.", ["https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500"]),
        ("Ripped Jeans", 2399, "Trendy ripped jeans. Distressed finish.", ["https://images.unsplash.com/photo-1542272604-787c3835535d?w=500"]),
        ("Corduroy Pants", 2099, "Classic corduroy pants. Warm and stylish.", ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500"]),
        ("Track Pants", 1299, "Athletic track pants with side stripes.", ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"]),
        ("Pleated Trousers", 2199, "Classic pleated formal trousers.", ["https://images.unsplash.com/photo-1594633313593-bab3825d0caf?w=500"]),
        ("Denim Shorts", 1399, "Casual denim shorts. Perfect for summer.", ["https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500"]),
        ("Khaki Chinos", 1899, "Classic khaki chinos. Versatile and comfortable.", ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500"]),
        ("Stretch Jeans", 2299, "Super stretch jeans for maximum comfort.", ["https://images.unsplash.com/photo-1542272604-787c3835535d?w=500"]),
        
        # Jackets & Outerwear (8 products)
        ("Leather Jacket", 5999, "Genuine leather jacket. Classic biker style.", ["https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500"]),
        ("Bomber Jacket", 3499, "Trendy bomber jacket with ribbed cuffs.", ["https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"]),
        ("Puffer Jacket", 4299, "Warm puffer jacket for winter. Water-resistant.", ["https://images.unsplash.com/photo-1544923408-75c5cef46f14?w=500"]),
        ("Denim Jacket Classic", 2799, "Timeless denim jacket. Perfect for layering.", ["https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500"]),
        ("Windbreaker", 2299, "Lightweight windbreaker. Packable design.", ["https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"]),
        ("Blazer Formal", 4999, "Tailored blazer for formal occasions.", ["https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500"]),
        ("Hoodie Jacket", 1999, "Comfortable hoodie jacket with zipper.", ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"]),
        ("Trench Coat", 5499, "Classic trench coat. Water-resistant.", ["https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500"]),
        
        # Shoes (5 products)
        ("Leather Formal Shoes", 3499, "Premium leather formal shoes. Perfect for office.", ["https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=500"]),
        ("Casual Sneakers", 2499, "Comfortable casual sneakers. All-day wear.", ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"]),
        ("Loafers Brown", 2999, "Classic brown loafers. Slip-on design.", ["https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500"]),
        ("Sports Running Shoes", 3999, "High-performance running shoes with cushioning.", ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"]),
        ("Canvas Shoes", 1799, "Casual canvas shoes. Lightweight and breathable.", ["https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500"]),
    ],
    
    "Women's Fashion": [
        # Dresses (12 products)
        ("Floral Maxi Dress", 2499, "Beautiful floral maxi dress. Perfect for summer.", ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500", "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500"]),
        ("Little Black Dress", 2999, "Classic LBD. Perfect for any occasion.", ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500"]),
        ("Cocktail Party Dress", 3499, "Elegant cocktail dress with sequin details.", ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500"]),
        ("Casual Sundress", 1799, "Light and breezy sundress for casual outings.", ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500"]),
        ("Wrap Dress", 2299, "Flattering wrap dress. Adjustable fit.", ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500"]),
        ("A-Line Dress", 2199, "Classic a-line dress. Timeless style.", ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500"]),
        ("Midi Dress Elegant", 2699, "Sophisticated midi dress for formal events.", ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500"]),
        ("Bodycon Dress", 2399, "Fitted bodycon dress. Party ready.", ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500"]),
        ("Shirt Dress", 1999, "Comfortable shirt dress. Versatile styling.", ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500"]),
        ("Printed Summer Dress", 2099, "Vibrant printed dress for summer.", ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500"]),
        ("Off-Shoulder Dress", 2599, "Trendy off-shoulder dress. Perfect for parties.", ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500"]),
        ("Denim Dress", 2199, "Casual denim dress. All-season wear.", ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500"]),
        
        # Tops & Blouses (10 products)
        ("Silk Blouse", 1899, "Elegant silk blouse. Perfect for office.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        ("Crop Top", 899, "Trendy crop top. Perfect for casual wear.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Peplum Top", 1599, "Flattering peplum top. Feminine silhouette.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        ("Tank Top Pack", 799, "Comfortable tank tops. Pack of 3.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Chiffon Blouse", 1699, "Lightweight chiffon blouse. Elegant drape.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        ("Tunic Top", 1399, "Comfortable tunic top. Perfect for leggings.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        ("Halter Neck Top", 1299, "Stylish halter neck top. Summer essential.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Embroidered Top", 1799, "Beautiful embroidered top. Ethnic touch.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        ("Cold Shoulder Top", 1499, "Trendy cold shoulder top. Modern style.", ["https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500"]),
        ("Button-Down Shirt", 1599, "Classic button-down shirt. Versatile piece.", ["https://images.unsplash.com/photo-1564257577-3a93c4f3e6c9?w=500"]),
        
        # Bottoms (8 products)
        ("High-Waist Jeans", 2299, "Flattering high-waist jeans. Stretch denim.", ["https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500"]),
        ("Palazzo Pants", 1799, "Flowy palazzo pants. Comfortable and stylish.", ["https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500"]),
        ("Pencil Skirt", 1599, "Classic pencil skirt. Office appropriate.", ["https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500"]),
        ("Leggings Pack", 999, "Comfortable leggings. Pack of 2.", ["https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=500"]),
        ("Culottes", 1899, "Trendy culottes. Wide-leg design.", ["https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500"]),
        ("Denim Shorts", 1299, "Casual denim shorts. Summer essential.", ["https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500"]),
        ("Maxi Skirt", 1999, "Flowy maxi skirt. Bohemian style.", ["https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500"]),
        ("Skinny Jeans", 2199, "Classic skinny jeans. Stretchy fabric.", ["https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500"]),
        
        # Shoes & Accessories (10 products)
        ("Heeled Sandals", 2499, "Elegant heeled sandals. Perfect for parties.", ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"]),
        ("Ballet Flats", 1799, "Comfortable ballet flats. All-day wear.", ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"]),
        ("Ankle Boots", 3499, "Stylish ankle boots. Versatile footwear.", ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"]),
        ("Designer Handbag", 4999, "Premium designer handbag. Genuine leather.", ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500"]),
        ("Crossbody Bag", 2299, "Compact crossbody bag. Perfect for outings.", ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500"]),
        ("Tote Bag", 1999, "Spacious tote bag. Daily essential.", ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500"]),
        ("Sunglasses Designer", 1599, "Trendy designer sunglasses. UV protection.", ["https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500"]),
        ("Fashion Watch", 2999, "Elegant fashion watch. Stainless steel.", ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"]),
        ("Scarf Silk", 899, "Luxurious silk scarf. Multiple colors.", ["https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=500"]),
        ("Statement Necklace", 1299, "Bold statement necklace. Party accessory.", ["https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500"]),
    ],
    
    "Electronics": [
        # Smartphones & Tablets (10 products)
        ("Smartphone Pro Max", 79999, "Flagship smartphone with 5G. 256GB storage.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500", "https://images.unsplash.com/photo-1592286927505-c80d3b4b8f40?w=500"]),
        ("Budget Smartphone", 12999, "Affordable smartphone with great features. 64GB.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"]),
        ("Gaming Phone", 45999, "High-performance gaming phone. 120Hz display.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"]),
        ("Tablet 10-inch", 24999, "Versatile tablet for work and entertainment.", ["https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500"]),
        ("iPad Alternative", 34999, "Premium tablet with stylus support.", ["https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500"]),
        ("Foldable Phone", 89999, "Innovative foldable smartphone. Latest tech.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"]),
        ("Mid-Range Phone", 22999, "Best value smartphone. 128GB storage.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"]),
        ("Camera Phone", 39999, "Photography-focused smartphone. 108MP camera.", ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"]),
        ("Kids Tablet", 8999, "Educational tablet for children. Parental controls.", ["https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500"]),
        ("E-Reader Tablet", 14999, "E-ink display tablet for reading. Eye-friendly.", ["https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500"]),
        
        # Laptops & Computers (8 products)
        ("Gaming Laptop", 89999, "High-performance gaming laptop. RTX graphics.", ["https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500"]),
        ("Ultrabook Slim", 65999, "Ultra-thin laptop. Perfect for professionals.", ["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"]),
        ("Budget Laptop", 32999, "Affordable laptop for students. 8GB RAM.", ["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"]),
        ("MacBook Alternative", 75999, "Premium laptop with aluminum body.", ["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"]),
        ("2-in-1 Laptop", 54999, "Convertible laptop and tablet. Touchscreen.", ["https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500"]),
        ("Desktop PC Gaming", 99999, "Custom gaming PC. RGB lighting.", ["https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500"]),
        ("All-in-One PC", 59999, "Space-saving all-in-one computer. 24-inch.", ["https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500"]),
        ("Chromebook", 25999, "Fast and secure Chromebook. Cloud-based.", ["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"]),
        
        # Audio & Accessories (12 products)
        ("Wireless Earbuds Pro", 8999, "Premium wireless earbuds. ANC and transparency mode.", ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500"]),
        ("Over-Ear Headphones", 12999, "Studio-quality headphones. 40-hour battery.", ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"]),
        ("Bluetooth Speaker", 4999, "Portable Bluetooth speaker. Waterproof.", ["https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500"]),
        ("Soundbar", 15999, "Home theater soundbar. Dolby Atmos.", ["https://images.unsplash.com/photo-1545454675-3531b543be5d?w=500"]),
        ("Wireless Mouse", 1299, "Ergonomic wireless mouse. Silent clicks.", ["https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500"]),
        ("Mechanical Keyboard", 5999, "RGB mechanical keyboard. Gaming grade.", ["https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500"]),
        ("Webcam HD", 3499, "1080p webcam for video calls. Auto-focus.", ["https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=500"]),
        ("USB Hub", 1499, "7-port USB hub. Fast data transfer.", ["https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500"]),
        ("External SSD 1TB", 7999, "Portable SSD. Lightning-fast speeds.", ["https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500"]),
        ("Phone Case Premium", 799, "Protective phone case. Shockproof design.", ["https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=500"]),
        ("Screen Protector", 399, "Tempered glass screen protector. 9H hardness.", ["https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=500"]),
        ("Charging Cable Pack", 599, "Fast charging cables. Pack of 3.", ["https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500"]),
        
        # Smart Devices (10 products)
        ("Smart Watch Ultra", 24999, "Advanced smartwatch. Health tracking.", ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"]),
        ("Fitness Band", 3999, "Affordable fitness tracker. Heart rate monitor.", ["https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500"]),
        ("Smart Home Hub", 8999, "Control all smart devices. Voice assistant.", ["https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=500"]),
        ("Security Camera", 5999, "WiFi security camera. Night vision.", ["https://images.unsplash.com/photo-1557324232-b8917d3c3dcb?w=500"]),
        ("Smart Bulb Pack", 2499, "RGB smart bulbs. Pack of 4. App control.", ["https://images.unsplash.com/photo-1550985616-10810253b84d?w=500"]),
        ("Video Doorbell", 9999, "Smart video doorbell. Two-way audio.", ["https://images.unsplash.com/photo-1558002038-1055907df827?w=500"]),
        ("Air Purifier Smart", 12999, "Smart air purifier. HEPA filter. App control.", ["https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500"]),
        ("Robot Vacuum", 18999, "Smart robot vacuum. Auto-charging.", ["https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500"]),
        ("Smart Thermostat", 7999, "Energy-saving smart thermostat. WiFi enabled.", ["https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=500"]),
        ("Smart Plug Pack", 1999, "WiFi smart plugs. Pack of 4. Voice control.", ["https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=500"]),
    ],
    
    "Home & Kitchen": [
        # Kitchen Appliances (15 products)
        ("Air Fryer 5L", 6999, "Healthy air fryer. Oil-free cooking. 1400W.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Microwave Oven", 8999, "Convection microwave. 28L capacity.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Blender High-Speed", 4999, "Professional blender. 1000W motor.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Coffee Maker", 5499, "Automatic coffee maker. 12-cup capacity.", ["https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"]),
        ("Toaster 4-Slice", 2999, "Stainless steel toaster. 7 browning levels.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Food Processor", 7999, "Multi-function food processor. 10 attachments.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Rice Cooker", 3499, "Electric rice cooker. 1.8L capacity.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Induction Cooktop", 4999, "Portable induction cooktop. Touch controls.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Mixer Grinder", 5999, "Powerful mixer grinder. 750W. 3 jars.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Sandwich Maker", 1999, "Non-stick sandwich maker. Compact design.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Juicer Cold Press", 8999, "Slow juicer. Maximum nutrient extraction.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Kettle Electric 1.7L", 1799, "Fast-boiling kettle. Auto shut-off.", ["https://images.unsplash.com/photo-1563822249366-7efbeb0d7e46?w=500"]),
        ("Hand Mixer", 2499, "Electric hand mixer. 5 speed settings.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Waffle Maker", 2799, "Belgian waffle maker. Non-stick plates.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        ("Egg Boiler", 1299, "Electric egg boiler. 7-egg capacity.", ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"]),
        
        # Cookware (12 products)
        ("Non-Stick Cookware Set", 7999, "12-piece non-stick cookware set. Induction compatible.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Pressure Cooker 5L", 3499, "Stainless steel pressure cooker. Safety features.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Cast Iron Skillet", 2999, "Pre-seasoned cast iron skillet. 12-inch.", ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"]),
        ("Wok Pan", 1999, "Carbon steel wok. Perfect for stir-fry.", ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"]),
        ("Sauce Pan Set", 4999, "Stainless steel sauce pans. Set of 3.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Grill Pan", 2499, "Non-stick grill pan. Indoor grilling.", ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"]),
        ("Dutch Oven", 5999, "Enameled cast iron dutch oven. 6-quart.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Frying Pan Set", 3999, "Non-stick frying pans. Set of 3 sizes.", ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"]),
        ("Kadai Heavy Bottom", 1799, "Traditional kadai. Heavy bottom design.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Tawa Non-Stick", 999, "Non-stick tawa. Perfect for rotis.", ["https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=500"]),
        ("Steamer Pot", 2299, "Multi-tier steamer. Healthy cooking.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        ("Casserole Set", 4499, "Insulated casserole set. Keeps food hot.", ["https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500"]),
        
        # Dinnerware & Storage (13 products)
        ("Dinner Set 32-Piece", 5999, "Elegant dinner set for 8. Microwave safe.", ["https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=500"]),
        ("Glass Storage Set", 2999, "Borosilicate glass containers. Set of 10.", ["https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"]),
        ("Cutlery Set", 3499, "Stainless steel cutlery. 24-piece set.", ["https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=500"]),
        ("Wine Glasses Set", 1999, "Crystal wine glasses. Set of 6.", ["https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=500"]),
        ("Coffee Mugs Set", 1299, "Ceramic coffee mugs. Set of 6.", ["https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500"]),
        ("Serving Bowls", 2499, "Decorative serving bowls. Set of 3.", ["https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=500"]),
        ("Plastic Containers", 1499, "Airtight plastic containers. Set of 12.", ["https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"]),
        ("Spice Rack", 1799, "Rotating spice rack. 16 jars included.", ["https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"]),
        ("Knife Set", 4999, "Professional knife set. 8 pieces with block.", ["https://images.unsplash.com/photo-1593618998160-e34014e67546?w=500"]),
        ("Cutting Board Set", 1999, "Bamboo cutting boards. Set of 3 sizes.", ["https://images.unsplash.com/photo-1593618998160-e34014e67546?w=500"]),
        ("Mixing Bowls", 1599, "Stainless steel mixing bowls. Set of 5.", ["https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=500"]),
        ("Measuring Cups", 799, "Measuring cups and spoons. Complete set.", ["https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"]),
        ("Lunch Box", 899, "Stainless steel lunch box. 3 compartments.", ["https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"]),
    ],
    
    "Sports & Outdoor": [
        # Fitness Equipment (15 products)
        ("Treadmill Motorized", 34999, "Foldable treadmill. 2HP motor. LCD display.", ["https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=500"]),
        ("Exercise Bike", 18999, "Stationary exercise bike. Adjustable resistance.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Dumbbell Set Adjustable", 8999, "Adjustable dumbbells 5-25kg. Space-saving.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Yoga Mat Premium", 1999, "Extra thick yoga mat. Non-slip. Eco-friendly.", ["https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"]),
        ("Resistance Bands Set", 1299, "Resistance bands. 5 levels. With handles.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        ("Pull-Up Bar", 1999, "Doorway pull-up bar. No drilling required.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Ab Roller Wheel", 799, "Ab roller with knee pad. Core strengthening.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Kettlebell Set", 4999, "Cast iron kettlebells. 8kg, 12kg, 16kg.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Foam Roller", 1499, "High-density foam roller. Muscle recovery.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        ("Jump Rope", 599, "Speed jump rope. Adjustable length. Ball bearings.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        ("Push-Up Bars", 899, "Push-up stands. Ergonomic grip.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Weight Bench", 12999, "Adjustable weight bench. Multi-position.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Medicine Ball", 1999, "Weighted medicine ball. 5kg. Textured grip.", ["https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"]),
        ("Balance Board", 2499, "Wooden balance board. Core stability training.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        ("Gym Gloves", 799, "Workout gloves. Wrist support. Breathable.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        
        # Outdoor Gear (12 products)
        ("Camping Tent 6-Person", 9999, "Waterproof tent. Easy setup. UV protection.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Sleeping Bag", 2999, "3-season sleeping bag. Compact and warm.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Backpack 60L", 4999, "Hiking backpack. Rain cover included.", ["https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"]),
        ("Camping Stove", 3499, "Portable camping stove. Gas powered.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Headlamp LED", 1299, "Rechargeable headlamp. 1000 lumens.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Trekking Poles", 1999, "Adjustable trekking poles. Pair. Shock absorbing.", ["https://images.unsplash.com/photo-1551632811-561732d1e306?w=500"]),
        ("Camping Chair", 1799, "Foldable camping chair. Cup holder.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Cooler Box 50L", 3999, "Insulated cooler box. Keeps ice for 5 days.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Water Bottle 1L", 799, "Insulated water bottle. Leak-proof.", ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"]),
        ("Hammock", 1999, "Portable hammock. Supports 200kg.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Binoculars", 3999, "10x42 binoculars. HD optics. Waterproof.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        ("Compass", 599, "Military-grade compass. Waterproof.", ["https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500"]),
        
        # Sports Equipment (13 products)
        ("Mountain Bike 29-inch", 24999, "21-speed mountain bike. Disc brakes. Suspension.", ["https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500"]),
        ("Road Bike", 32999, "Lightweight road bike. Carbon fiber frame.", ["https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500"]),
        ("Bicycle Helmet", 1499, "Safety helmet. Adjustable fit. Ventilated.", ["https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500"]),
        ("Football Size 5", 899, "Professional football. FIFA approved.", ["https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=500"]),
        ("Basketball", 1299, "Indoor/outdoor basketball. Official size.", ["https://images.unsplash.com/photo-1546519638-68e109498ffc?w=500"]),
        ("Cricket Bat", 2999, "Kashmir willow cricket bat. Full size.", ["https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=500"]),
        ("Badminton Racket Set", 2499, "Professional badminton rackets. Pair with shuttles.", ["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=500"]),
        ("Tennis Racket", 3499, "Graphite tennis racket. Intermediate level.", ["https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500"]),
        ("Skateboard", 2999, "Complete skateboard. ABEC-9 bearings.", ["https://images.unsplash.com/photo-1547447134-cd3f5c716030?w=500"]),
        ("Swimming Goggles", 799, "Anti-fog swimming goggles. UV protection.", ["https://images.unsplash.com/photo-1530549387789-4c1017266635?w=500"]),
        ("Boxing Gloves", 1999, "Training boxing gloves. 12oz. Padded.", ["https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=500"]),
        ("Skipping Rope Pro", 899, "Professional skipping rope. Weighted handles.", ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"]),
        ("Yoga Block Set", 799, "Foam yoga blocks. Set of 2. With strap.", ["https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"]),
    ],
}

# Generate products
print("\n[4/4] Creating products with variants...")
total_created = 0
category_counts = {}

for category_name, products in products_templates.items():
    category = Category.objects.get(category_name=category_name)
    category_count = 0
    
    for prod_name, price, description, images in products:
        product, created = Product.objects.get_or_create(
            product_name=prod_name,
            defaults={
                "category": category,
                "price": price,
                "product_desription": description,
                "newest_product": random.choice([True, False])
            }
        )
        
        if created:
            # Add images
            for img_url in images:
                ProductImage.objects.create(product=product, image_url=img_url)
            
            # Add color variants for applicable products
            if category_name in ["Men's Fashion", "Women's Fashion"]:
                num_colors = random.randint(3, 6)
                selected_colors = random.sample(color_objects, num_colors)
                product.color_variant.set(selected_colors)
            
            # Add size variants for clothing
            if "Shirt" in prod_name or "T-Shirt" in prod_name or "Dress" in prod_name or "Top" in prod_name or "Pant" in prod_name or "Jean" in prod_name or "Jacket" in prod_name:
                sizes = SizeVariant.objects.all()
                product.size_variant.set(sizes)
            
            total_created += 1
            category_count += 1
    
    category_counts[category_name] = category_count
    print(f"  ✓ {category_name}: {category_count} products")

print("\n" + "="*60)
print("DATABASE POPULATION COMPLETE!")
print("="*60)
print(f"\n📊 Summary:")
print(f"  • Total Products Created: {total_created}")
print(f"  • Total Categories: {Category.objects.count()}")
print(f"  • Total Product Images: {ProductImage.objects.count()}")
print(f"  • Color Variants: {ColorVariant.objects.count()}")
print(f"  • Size Variants: {SizeVariant.objects.count()}")
print(f"\n✅ Your RetailX store is now fully stocked!")
print("="*60)
