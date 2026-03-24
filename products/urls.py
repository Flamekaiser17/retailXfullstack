from django.urls import path
from products.views import *

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<uid>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/move_to_cart/<uid>/', move_to_cart, name='move_to_cart'),
    path('wishlist/remove/<uid>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('product-reviews/', product_reviews, name='product_reviews'),
    path('product-reviews/edit/<uuid:review_uid>/', edit_review, name='edit_review'),
    path('like-review/<review_uid>/', like_review, name='like_review'),
    path('dislike-review/<review_uid>/',dislike_review, name='dislike_review'),
    path('notify/<product_uid>/', stock_notification_signup, name='stock_notification'),
    path('check-inventory/', check_inventory_ajax, name='check_inventory'),
    path('set-price-alert/', create_price_alert_ajax, name='set_price_alert'),
    path('<slug>/', get_product, name='get_product'),
    path('<slug>/<review_uid>/delete/', delete_review, name='delete_review'),
]

# Wishlist → Cart
# Real ecommerce feature (🔥 interview point)