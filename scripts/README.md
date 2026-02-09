# Scripts Directory

This folder contains utility scripts for managing the RetailX eCommerce database.

## Available Scripts

### 1. `add_size_variants.py`
Adds size variants (S, M, L, XL, XXL) to all fashion products (Men's and Women's categories).

**Usage:**
```bash
python scripts/add_size_variants.py
```

**What it does:**
- Finds all products in Men's Fashion and Women's Fashion categories
- Adds 5 size variants to each product
- Updates 80+ products automatically

---

### 2. `add_multiple_images.py`
Adds multiple product images (2-3 images) to products for gallery view.

**Usage:**
```bash
python scripts/add_multiple_images.py
```

**What it does:**
- Adds 2-3 images per product from Unsplash
- Creates image gallery for product pages
- Updates 50+ products across all categories

---

### 3. `populate_products.py`
Populates the database with initial product data across multiple categories.

**Usage:**
```bash
python scripts/populate_products.py
```

**What it does:**
- Creates products in various categories (Electronics, Fashion, Home, etc.)
- Adds product details, prices, descriptions
- Sets up initial inventory

---

### 4. `populate_products_advanced.py`
Advanced product population script with comprehensive product data and categories.

**Usage:**
```bash
python scripts/populate_products_advanced.py
```

**What it does:**
- Creates 100+ products across multiple categories
- Adds detailed descriptions and specifications
- Sets up comprehensive product catalog
- Includes pricing and inventory data

---

### 5. `update_product_details.py`
Updates existing products with enhanced descriptions and details.

**Usage:**
```bash
python scripts/update_product_details.py
```

**What it does:**
- Enhances product descriptions
- Updates product specifications
- Improves product information quality

---

## Running Scripts

**Local Development:**
```bash
cd d:\Ecommerce
python scripts/script_name.py
```

**On Render (via Shell):**
```bash
python scripts/script_name.py
```

---

## Notes

- All scripts use Django ORM and require `DJANGO_SETTINGS_MODULE` to be set
- Scripts are idempotent where possible (safe to run multiple times)
- Check script output for success/error messages
