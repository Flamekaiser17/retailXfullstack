import json
import random
from .forms import ReviewForm
from django.urls import reverse
from django.contrib import messages
from accounts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, SizeVariant, ProductReview, Wishlist, PriceHistory

# Create your views here.

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    sorted_size_variants = product.size_variant.all().order_by('size_name')
    related_products = list(product.category.products.filter(parent=None).exclude(uid=product.uid))

    # Review product view
    review = None
    if request.user.is_authenticated:
        try:
            review = ProductReview.objects.filter(product=product, user=request.user).first()
        except Exception as e:
            print("No reviews found for this product", str(e))

    rating_percentage = 0
    if product.reviews.exists():
        rating_percentage = (product.get_rating() / 5) * 100

    has_purchased = False
    if request.user.is_authenticated:
        from accounts.models import OrderItem
        has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if not has_purchased:
            messages.error(request, "Only verified buyers can review this product.")
            return redirect('get_product', slug=slug)
            
        if review:
            review_form = ReviewForm(request.POST, instance=review)
        else:
            review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect('get_product', slug=slug)
    else:
        review_form = ReviewForm()

    # Related product view
    if len(related_products) >= 4:
        related_products = random.sample(related_products, 4)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    # Price History — unique RetailX feature
    price_history_qs = PriceHistory.objects.filter(product=product).order_by('recorded_at')
    price_history_labels = json.dumps([
        ph.recorded_at.strftime('%d %b %Y') for ph in price_history_qs
    ])
    price_history_values = json.dumps([ph.price for ph in price_history_qs])
    lowest_price = price_history_qs.order_by('price').first()
    highest_price = price_history_qs.order_by('-price').first()

    # Active flash sale for this product
    from django.utils import timezone
    now = timezone.now()
    active_flash_sale = product.flash_sales.filter(
        is_active=True, start_time__lte=now, end_time__gte=now
    ).first()

    # Complete the Look Algorithm
    # Suggest 4 random products that are NOT in the same category (e.g., matching pants/shoes for a shirt)
    complete_the_look = Product.objects.exclude(category=product.category).exclude(uid=product.uid).order_by('?')[:4]

    # Smart Size Recommendation
    recommended_size = None
    if request.user.is_authenticated:
        from accounts.models import OrderItem
        past_item = OrderItem.objects.filter(
            order__user=request.user,
            product__category=product.category,
            size_variant__isnull=False
        ).order_by('-order__order_date').first()
        
        if past_item:
            recommended_size = past_item.size_variant.size_name

    context = {
        'product': product,
        'sorted_size_variants': sorted_size_variants,
        'related_products': related_products,
        'review_form': review_form,
        'rating_percentage': rating_percentage,
        'in_wishlist': in_wishlist,
        'price_history_labels': price_history_labels,
        'price_history_values': price_history_values,
        'price_history_json': json.dumps([
            {'date': ph.recorded_at.strftime('%d %b %Y'), 'price': float(ph.price)} 
            for ph in price_history_qs
        ]),
        'lowest_price': lowest_price,
        'highest_price': highest_price,
        'active_flash_sale': active_flash_sale,
        'has_purchased': has_purchased,
        'complete_the_look': complete_the_look,
        'recommended_size': recommended_size,
    }

    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price

    return render(request, 'product/product.html', context=context)


# Product Review view
@login_required
def product_reviews(request):
    reviews = ProductReview.objects.filter(
        user=request.user).select_related('product').order_by('-date_added')
    return render(request, 'product/all_product_reviews.html', {'reviews': reviews})


# Edit Review view
@login_required
def edit_review(request, review_uid):
    review = ProductReview.objects.filter(uid=review_uid, user=request.user).first()
    if not review:
        return JsonResponse({"detail": "Review not found"}, status=404)
    
    if request.method == "POST":
        stars = request.POST.get("stars")
        content = request.POST.get("content")
        review.stars = stars
        review.content = content
        review.save()
        messages.success(request, "Your review has been updated successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return JsonResponse({"detail": "Invalid request"}, status=400)

# Like and Dislike review view
def like_review(request, review_uid):
    review = ProductReview.objects.filter(uid=review_uid).first()

    if request.user in review.likes.all():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
        review.dislikes.remove(request.user)
    return JsonResponse({'likes': review.like_count(), 'dislikes': review.dislike_count()})


def dislike_review(request, review_uid):
    review = ProductReview.objects.filter(uid=review_uid).first()

    if request.user in review.dislikes.all():
        review.dislikes.remove(request.user)
    else:
        review.dislikes.add(request.user)
        review.likes.remove(request.user)
    return JsonResponse({'likes': review.like_count(), 'dislikes': review.dislike_count()})


# delete review view
def delete_review(request, slug, review_uid):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to delete a review.")
        return redirect('login')

    review = ProductReview.objects.filter(uid=review_uid, product__slug=slug, user=request.user).first()
    
    if not review:
        messages.error(request, "Review not found.")
        return redirect('get_product', slug=slug)

    review.delete()
    messages.success(request, "Your review has been deleted.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Add a product to Wishlist
@login_required
def add_to_wishlist(request, uid):
    variant = request.GET.get('size')
    if not variant:
        messages.warning(request, 'Please select a size variant before adding to the wishlist!')
        return redirect(request.META.get('HTTP_REFERER'))

    product = get_object_or_404(Product, uid=uid)
    size_variant = get_object_or_404(SizeVariant, size_name=variant)
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user, product=product, size_variant=size_variant)

    if created:
        messages.success(request, "Product added to Wishlist!")

    return redirect(reverse('wishlist'))


# Remove product from wishlist
@login_required
def remove_from_wishlist(request, uid):
    product = get_object_or_404(Product, uid=uid)
    size_variant_name = request.GET.get('size')

    if size_variant_name:
        size_variant = get_object_or_404(SizeVariant, size_name=size_variant_name)
        Wishlist.objects.filter(
            user=request.user, product=product, size_variant=size_variant).delete()
    else:
        Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.success(request, "Product removed from wishlist!")
    return redirect(reverse('wishlist'))


# Wishlist View
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items})


# Move to cart functionality on wishlist page.
def move_to_cart(request, uid):
    product = get_object_or_404(Product, uid=uid)
    wishlist = Wishlist.objects.filter(user=request.user, product=product).first()

    if not wishlist:
        messages.error(request, "Item not found in wishlist.")
        return redirect('wishlist')

    size_variant = wishlist.size_variant
    wishlist.delete()

    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size_variant=size_variant)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product moved to cart successfully!")
    return redirect('cart')


# Stock Notification Signup
def stock_notification_signup(request, product_uid):
    """AJAX endpoint for stock notification signup"""
    if request.method == 'POST':
        from products.models import StockNotification
        import json
        
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            
            if not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Please provide a valid email address.'
                }, status=400)
            
            product = get_object_or_404(Product, uid=product_uid)
            
            # Create or get notification
            notification, created = StockNotification.objects.get_or_create(
                email=email,
                product=product
            )
            
            if created:
                return JsonResponse({
                    'success': True,
                    'message': f'Great! We\'ll notify you at {email} when {product.product_name} is back in stock.'
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'You\'re already subscribed to notifications for this product.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)


def check_inventory_ajax(request):
    try:
        data = json.loads(request.body)
        product_slug = data.get('slug')
        size = data.get('size')
        
        product = get_object_or_404(Product, slug=product_slug)
        # For RetailX we assume base stock is tracked via product.stock
        out_of_stock = product.stock <= 0
            
        return JsonResponse({"success": True, "out_of_stock": out_of_stock})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def create_price_alert_ajax(request):
    """Handle creating or updating a price alert via AJAX."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
    try:
        data = json.loads(request.body)
        product_slug = data.get('slug')
        target_price = data.get('target_price')
        
        if not target_price or not product_slug:
            return JsonResponse({'success': False, 'message': 'Missing data'}, status=400)
            
        try:
            target_price = int(target_price)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid price format'}, status=400)
            
        product = get_object_or_404(Product, slug=product_slug)
        
        from .models import PriceAlert
        alert, created = PriceAlert.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'target_price': target_price, 'is_active': True}
        )
        
        return JsonResponse({
            'success': True, 
            'message': f'Alert set! We will email you when {product.product_name} drops below ₹{target_price}.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
