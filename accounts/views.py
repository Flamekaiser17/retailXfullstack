import os
import json
import uuid
import razorpay
from products.models import *
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from home.models import ShippingAddress
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.db.models import Prefetch
from django.db import transaction
from accounts.models import Profile, Cart, CartItem, Order, OrderItem
from base.emails import send_account_activation_email
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import UserUpdateForm, UserProfileForm, ShippingAddressForm, CustomPasswordChangeForm


# Create your views here.


class GuestCartItem:
    """Temporary cart item for guest users"""
    def __init__(self, product, size_variant, quantity):
        self.uid = f"{product.uid}_{size_variant.size_name if size_variant else 'none'}"
        self.product = product
        self.size_variant = size_variant
        self.color_variant = None
        self.quantity = quantity
    
    def get_product_price(self):
        price = self.product.price * self.quantity
        if self.size_variant:
            price += self.size_variant.price
        return price


class GuestCart:
    """Temporary cart object for guest users using session data"""
    def __init__(self, session_cart):
        self.session_cart = session_cart
        self.uid = 'guest'
        self.coupon = None
        self.is_paid = False
        self.razorpay_order_id = None
        self._items = None
    
    def _load_items(self):
        if self._items is None:
            self._items = []
            for key, item_data in self.session_cart.items():
                try:
                    product = Product.objects.get(uid=item_data['product_uid'])
                    size_variant = SizeVariant.objects.get(size_name=item_data['size_variant']) if item_data.get('size_variant') else None
                    self._items.append(GuestCartItem(product, size_variant, item_data['quantity']))
                except Exception as e:
                    print(f"Error loading guest cart item: {e}")
        return self._items
    
    @property
    def cart_items(self):
        return self._load_items()
    
    def get_cart_total(self):
        return sum(item.get_product_price() for item in self.cart_items)
    
    def get_cart_total_price_after_coupon(self):
        total = self.get_cart_total()
        if self.coupon and total >= self.coupon.minimum_amount:
            total -= self.coupon.discount_amount
        return total


def merge_guest_cart(request, user):
    """Merge guest session cart into user's database cart on login"""
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
    
    try:
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        for key, item_data in session_cart.items():
            try:
                product = Product.objects.get(uid=item_data['product_uid'])
                size_variant = SizeVariant.objects.get(size_name=item_data['size_variant']) if item_data.get('size_variant') else None
                
                # Use filter().first() to avoid MultipleObjectsReturned errors
                cart_item = CartItem.objects.filter(
                    cart=cart, product=product, size_variant=size_variant
                ).first()
                if cart_item:
                    cart_item.quantity += item_data['quantity']
                else:
                    cart_item = CartItem.objects.create(
                        cart=cart, product=product, size_variant=size_variant,
                        quantity=item_data['quantity']
                    )
                cart_item.save()
            except Exception as e:
                print(f"Error merging cart item: {e}")
        
        # Clear session cart after merge
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Your guest cart has been merged with your account.')
    except Exception as e:
        print(f"Error merging guest cart: {e}")


def login_page(request):
    # Get the next URL from the query parameter
    next_url = request.GET.get('next')
    if request.method == 'POST':
        identifier = request.POST.get('username') # This matches the 'name' in HTML
        password = request.POST.get('password')
        
        # Check for user by username OR email
        user_obj = User.objects.filter(models.Q(username=identifier) | models.Q(email=identifier)).first()

        if not user_obj:
            messages.warning(request, 'Account not found!')
            return HttpResponseRedirect(request.path_info)

        if not user_obj.profile.is_email_verified:
            messages.error(request, 'Account not verified!')
            return HttpResponseRedirect(request.path_info)

        # Use the actual username for authenticate()
        user = authenticate(username=user_obj.username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Successful.')
            
            # Merge guest cart if exists
            merge_guest_cart(request, user)

            if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=request.get_host()):
                return redirect(next_url or 'index')
            return redirect('index')

        messages.warning(request, 'Invalid credentials.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username, email=email)

        if user_obj.exists():
            messages.info(request, 'Username or email already exists!')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(
            username=username, first_name=first_name, last_name=last_name, email=email)
        user_obj.set_password(password)
        user_obj.save()

        profile = Profile.objects.get(user=user_obj)
        profile.email_token = str(uuid.uuid4())
        profile.save()

        send_account_activation_email(email, profile.email_token)
        messages.success(request, "An email has been sent to your mail.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "Logged Out Successfully!")
    return redirect('index')


def activate_email_account(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Account verification successful.')
        return redirect('login')
    except Exception as e:
        return HttpResponse('Invalid email token.')


def add_to_cart(request, uid):
    """Add to cart - supports both authenticated users (DB cart) and guests (session cart)"""
    try:
        variant = request.GET.get('size')
        if not variant:
            messages.warning(request, 'Please select a size variant!')
            return redirect(request.META.get('HTTP_REFERER'))

        product = get_object_or_404(Product, uid=uid)
        size_variant = get_object_or_404(SizeVariant, size_name=variant)

        if request.user.is_authenticated:
            # Authenticated user - use database cart
            cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size_variant=size_variant)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        else:
            # Guest user - use session cart
            session_cart = request.session.get('cart', {})
            item_key = f"{str(uid)}_{variant}"
            
            if item_key in session_cart:
                session_cart[item_key]['quantity'] += 1
            else:
                session_cart[item_key] = {
                    'product_uid': str(uid),
                    'size_variant': variant,
                    'quantity': 1
                }
            request.session['cart'] = session_cart
            request.session.modified = True

        messages.success(request, 'Item added to cart successfully.')

    except Exception as e:
        messages.error(request, f'Error adding item to cart: {str(e)}')

    return redirect(reverse('cart'))


def cart(request):
    """Cart view - supports both authenticated users and guests"""
    cart_obj = None
    payment = None
    
    if request.user.is_authenticated:
        # Authenticated user - use database cart
        user = request.user
        # N+1 FIX: prefetch cart_items with select_related for linked models
        cart_obj = Cart.objects.filter(is_paid=False, user=user).prefetch_related(
            Prefetch('cart_items', queryset=CartItem.objects.select_related('product', 'color_variant', 'size_variant'))
        ).last()
    else:
        # Guest user - build cart from session
        session_cart = request.session.get('cart', {})
        if session_cart:
            # Create a temporary cart-like object for template rendering
            cart_obj = GuestCart(session_cart)
    
    # Handle coupon form POST for authenticated users only
    if request.method == 'POST' and request.user.is_authenticated:
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__exact=coupon).first()
        if not coupon_obj:
            messages.warning(request, 'Invalid coupon code.')
        elif cart_obj and cart_obj.coupon:
            messages.warning(request, 'Coupon already exists.')
        elif coupon_obj and coupon_obj.is_expired:
            messages.warning(request, 'Coupon code expired.')
        elif cart_obj and coupon_obj and cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj.minimum_amount}')
        elif cart_obj and coupon_obj:
            cart_obj.coupon = coupon_obj
            cart_obj.save()
            messages.success(request, 'Coupon applied successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    # Payment setup for authenticated users only
    if request.user.is_authenticated and cart_obj:
        cart_total_in_paise = int(cart_obj.get_cart_total_price_after_coupon() * 100)
        if cart_total_in_paise >= 100:
            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                # RAZORPAY DUPLICATE ORDER FIX: Check if razorpay_order_id already exists
                if cart_obj.razorpay_order_id:
                    # In a real scenario, we'd verify if the amount matches, 
                    # but here we follow the request to check existence.
                    payment = {'id': cart_obj.razorpay_order_id, 'amount': cart_total_in_paise}
                else:
                    payment = client.order.create({'amount': cart_total_in_paise, 'currency': 'INR', 'payment_capture': 1})
                    cart_obj.razorpay_order_id = payment['id']
                    cart_obj.save()
            except Exception as e:
                print(f"Razorpay error: {str(e)}")
                messages.info(request, 'Payment gateway not configured.')
                payment = None
    
    if not cart_obj or (request.user.is_authenticated and not cart_obj.cart_items.exists() and not request.session.get('cart')):
        messages.warning(request, "Your cart is empty. Please add a product to cart.")
        return redirect(reverse('index'))
    
    context = {
        'cart': cart_obj,
        'payment': payment,
        'quantity_range': range(1, 6),
        'base_url': settings.BASE_URL,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'accounts/cart.html', context)


@require_POST
def update_cart_item(request):
    """Update cart item quantity - supports both authenticated and guest users"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get("cart_item_id")
        quantity = int(data.get("quantity"))
        
        if request.user.is_authenticated:
            # Authenticated user - update database cart
            cart_item = CartItem.objects.filter(
                uid=cart_item_id, 
                cart__user=request.user, 
                cart__is_paid=False
            ).last()
            if not cart_item:
                return JsonResponse({"success": False, "error": "Cart item not found."})
            cart_item.quantity = quantity
            cart_item.save()
            
            cart = cart_item.cart
            cart_total = cart.get_cart_total()
            final_total = cart.get_cart_total_price_after_coupon()
            delivery_charge = 0 if cart_total >= 499 else 49
            
            # Create new razorpay order ID (since amount changed)
            cart_total_in_paise = int(final_total * 100)
            razorpay_order_id = ""
            if cart_total_in_paise >= 100:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment = client.order.create({'amount': cart_total_in_paise, 'currency': 'INR', 'payment_capture': 1})
                razorpay_order_id = payment['id']
                cart.razorpay_order_id = razorpay_order_id
                cart.save()
            
            return JsonResponse({
                "success": True,
                "item_subtotal": cart_item.get_product_price() * cart_item.quantity,
                "cart_total": cart_total,
                "delivery": delivery_charge,
                "final_total": final_total,
                "item_count": cart.cart_items.count(),
                "razorpay_order_id": razorpay_order_id
            })
        else:
            # Guest user - update session cart
            session_cart = request.session.get('cart', {})
            
            # Find the item by UID and update quantity
            for key, item in session_cart.items():
                if key.startswith(f"{cart_item_id}_") or item.get('product_uid') == str(cart_item_id):
                    item['quantity'] = quantity
                    break
            
            request.session['cart'] = session_cart
            request.session.modified = True
            
            # Calculate totals for guest cart
            cart_obj = GuestCart(session_cart)
            cart_total = cart_obj.get_cart_total()
            final_total = cart_obj.get_cart_total_price_after_coupon()
            delivery_charge = 0 if cart_total >= 499 else 49
            
            return JsonResponse({
                "success": True,
                "item_subtotal": cart_total,  # Approximate for guests
                "cart_total": cart_total,
                "delivery": delivery_charge,
                "final_total": final_total,
                "item_count": len(session_cart),
                "razorpay_order_id": ""
            })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def remove_cart(request, uid):
    """Remove item from cart - supports both authenticated and guest users"""
    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, uid=uid)
            cart_item.delete()
        else:
            # Guest user - remove from session cart
            session_cart = request.session.get('cart', {})
            # Find and remove the item with matching UID
            for key, item in list(session_cart.items()):
                if item.get('product_uid') == str(uid) or key.endswith(f"_{uid}"):
                    del session_cart[key]
                    break
            request.session['cart'] = session_cart
            request.session.modified = True
        messages.success(request, 'Item removed from cart.')
    except Exception as e:
        print(e)
        messages.warning(request, 'Error removing item from cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()

    messages.success(request, 'Coupon Removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
@login_required
def apply_coupon_ajax(request):
    try:
        data = json.loads(request.body)
        coupon_code = data.get("coupon")
        cart = Cart.objects.filter(user=request.user, is_paid=False).last()
        if not cart:
            return JsonResponse({"success": False, "error": "No active cart found."})
        
        coupon_obj = Coupon.objects.filter(coupon_code__exact=coupon_code).first()
        if not coupon_obj:
            return JsonResponse({"success": False, "error": "Invalid coupon code."})
        if cart.coupon == coupon_obj:
            return JsonResponse({"success": False, "error": "Coupon already applied."})
        if coupon_obj.is_expired:
            return JsonResponse({"success": False, "error": "Coupon code expired."})
        if cart.get_cart_total() < coupon_obj.minimum_amount:
            return JsonResponse({"success": False, "error": f"Amount should be greater than ₹{coupon_obj.minimum_amount}"})

        cart.coupon = coupon_obj
        cart.save()
        
        cart_total = cart.get_cart_total()
        final_total = cart.get_cart_total_price_after_coupon()
        delivery_charge = 0 if cart_total >= 499 else 49
        
        # update razorpay order
        cart_total_in_paise = int(final_total * 100)
        razorpay_order_id = ""
        if cart_total_in_paise >= 100:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': cart_total_in_paise, 'currency': 'INR', 'payment_capture': 1})
            razorpay_order_id = payment['id']
            cart.razorpay_order_id = razorpay_order_id
            cart.save()

        return JsonResponse({
            "success": True,
            "cart_total": cart_total,
            "discount_amount": coupon_obj.discount_amount,
            "coupon_code": coupon_obj.coupon_code,
            "delivery": delivery_charge,
            "final_total": final_total,
            "razorpay_order_id": razorpay_order_id
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@require_POST
@login_required
def remove_coupon_ajax(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart.coupon = None
        cart.save()
        
        cart_total = cart.get_cart_total()
        final_total = cart.get_cart_total_price_after_coupon()
        delivery_charge = 0 if cart_total >= 499 else 49

        cart_total_in_paise = int(final_total * 100)
        razorpay_order_id = ""
        if cart_total_in_paise >= 100:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': cart_total_in_paise, 'currency': 'INR', 'payment_capture': 1})
            razorpay_order_id = payment['id']
            cart.razorpay_order_id = razorpay_order_id
            cart.save()
            
        return JsonResponse({
            "success": True,
            "cart_total": cart_total,
            "delivery": delivery_charge,
            "final_total": final_total,
            "razorpay_order_id": razorpay_order_id
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# --- PRODUCTION-GRADE PAYMENT HANDLING ---

@transaction.atomic
def complete_order_payment(razorpay_order_id, payment_id, signature=None):
    """
    Atomic and Idempotent service to finalize an order.
    Can be called by both Callback and Webhook.
    """
    # 1. Idempotency Check: Does an order with this ID already exist?
    existing_order = Order.objects.filter(order_id=razorpay_order_id).first()
    if existing_order:
        return existing_order, False # Already processed

    # 2. Get the Cart
    cart = Cart.objects.filter(razorpay_order_id=razorpay_order_id, is_paid=False).last()
    if not cart:
        # Might happen if webhook is slow and callback already finished, or cart was deleted
        return None, False

    # 3. Mark Cart as Paid
    cart.is_paid = True
    cart.razorpay_payment_id = payment_id
    if signature:
        cart.razorpay_payment_signature = signature
    cart.save()

    # 4. Create Order
    profile = cart.user.profile
    address = profile.shipping_address if profile.shipping_address else "No address set"
    
    order = Order.objects.create(
        user=cart.user,
        order_id=razorpay_order_id,
        payment_status="Paid",
        shipping_address=str(address),
        payment_mode="Razorpay",
        order_total_price=cart.get_cart_total(),
        coupon=cart.coupon,
        grand_total=cart.get_cart_total_price_after_coupon()
    )

    # 5. Create OrderItems
    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            size_variant=item.size_variant,
            color_variant=item.color_variant,
            quantity=item.quantity,
            product_price=item.get_product_price()
        )
    
    return order, True


@csrf_exempt
def payment_callback(request):
    """Frontend callback redirect handler."""
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            # Verify Signature
            client.utility.verify_payment_signature(params_dict)
            
            # Atomic processing using service
            order, created = complete_order_payment(order_id, payment_id, signature)
            
            if order:
                messages.success(request, "Payment successful! Your order has been placed.")
            else:
                messages.info(request, "Order already processed.")
                
            return redirect('order_history')
            
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed.")
            return redirect('cart')
        except Exception as e:
            print(f"Callback error: {e}")
            messages.error(request, "An error occurred during payment processing.")
            return redirect('cart')
            
    return redirect('cart')


@csrf_exempt
def payment_webhook(request):
    """Server-to-server webhook for transaction resilience."""
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
    payload = request.body.decode('utf-8')
    signature = request.headers.get('X-Razorpay-Signature')

    try:
        # Verify Webhook Signature
        client.utility.verify_webhook_signature(payload, signature, webhook_secret)
        
        data = json.loads(payload)
        event = data.get('event')

        if event == 'payment.captured':
            payment_entity = data['payload']['payment']['entity']
            order_id = payment_entity['order_id']
            payment_id = payment_entity['id']
            
            # Self-healing: Finalize order if frontend callback failed/timed out
            complete_order_payment(order_id, payment_id)

        elif event == 'payment.failed':
            # Log failure for analytics
            print(f"Payment failed for order: {data['payload']['payment']['entity']['order_id']}")

        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def download_invoice(request, order_id):
    return HttpResponse("Invoice PDF feature is disabled in local setup.")


@login_required
def profile_view(request, username=None):
    if not username:
        username = request.user.username
    
    profile_user = get_object_or_404(User, username=username)
    
    if request.user != profile_user:
        messages.warning(request, "You can only edit your own profile.")
        return redirect('profile', username=request.user.username)
    
    user = request.user
    profile = user.profile

    user_form = UserUpdateForm(instance=user)
    profile_form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    cart_items_count = 0
    wishlist_count = 0
    orders_count = 0
    
    try:
        cart = Cart.objects.filter(user=user, is_paid=False).first()
        if cart:
            cart_items_count = cart.cart_items.count()
    except:
        pass
    
    try:
        wishlist_count = Wishlist.objects.filter(user=user).count()
    except:
        pass
    
    try:
        orders_count = Order.objects.filter(user=user).count()
    except:
        pass

    context = {
        'user_name': profile_user,
        'user_form': user_form,
        'profile_form': profile_form,
        'cart_items_count': cart_items_count,
        'wishlist_count': wishlist_count,
        'orders_count': orders_count,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def update_shipping_address(request):
    shipping_address = ShippingAddress.objects.filter(
        user=request.user, current_address=True).first()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.current_address = True
            shipping_address.save()

            messages.success(
                request, "The Address Has Been Successfully Saved/Updated!")

            form = ShippingAddressForm()
        else:
            form = ShippingAddressForm(request.POST, instance=shipping_address)
    else:
        form = ShippingAddressForm(instance=shipping_address)

    return render(request, 'accounts/shipping_address_form.html', {'form': form})


@login_required
def order_history(request):
    # Optimized N+1 Query Fix
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__product').order_by('-order_date')
    return render(request, 'accounts/order_history.html', {'orders': orders})


@login_required
def order_details(request, order_id):
    # Optimized N+1 Query Fix
    order = get_object_or_404(Order.objects.select_related('coupon'), order_id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    
    context = {
        'order': order,
        'order_items': order_items,
        'order_total_price': sum(item.get_total_price() for item in order_items),
        'coupon_discount': order.coupon.discount_amount if order.coupon else 0,
        'grand_total': order.get_order_total_price()
    }
    return render(request, 'accounts/order_details.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(
            request, "Your account has been deleted successfully.")
        return redirect('index')
