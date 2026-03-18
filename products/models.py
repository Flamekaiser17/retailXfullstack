from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name


class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size_name


class Product(BaseModel):
    parent = models.ForeignKey(
        'self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_desription = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    newest_product = models.BooleanField(default=False)
    stock = models.IntegerField(default=50)  # Default stock level

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name
# dynamic price based on size
    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size_name=size).price
# dynamic rating based on reviews
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image_url = models.URLField(
        max_length=500, default='https://via.placeholder.com/500')

    def img_preview(self):
        return mark_safe(f'<img src="{self.image_url}" width="500"/>')


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_amount = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)


class ProductReview(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(
        default=3, choices=[(i, i) for i in range(1, 6)])
    content = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="liked_reviews", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="disliked_reviews", blank=True)

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()


class Wishlist(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name="wishlist_items")

    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'size_variant')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.product.product_name} - {self.size_variant.size_name if self.size_variant else "No Size"}'


class StockNotification(BaseModel):
    """Model to store email notifications for out-of-stock products"""
    email = models.EmailField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_notifications")
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('email', 'product')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.email} - {self.product.product_name}'


class PriceHistory(BaseModel):
    """Tracks price changes over time — unique feature vs Amazon/Flipkart"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100, blank=True, default='')  # e.g. "Sale price", "Regular price"

    class Meta:
        ordering = ['recorded_at']

    def __str__(self) -> str:
        return f'{self.product.product_name} — ₹{self.price} on {self.recorded_at.strftime("%d %b %Y")}'


class FlashSale(BaseModel):
    """Flash sale model — creates urgency like Myntra's End of Reason Sale"""
    title = models.CharField(max_length=200)
    discount_percentage = models.IntegerField(default=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True, related_name='flash_sales')
    is_active = models.BooleanField(default=True)
    banner_color = models.CharField(max_length=20, default='#FF3F6C')

    def __str__(self) -> str:
        return self.title

    def is_live(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time
