from django.db.models import Q
from django.shortcuts import render
from products.models import Product, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def index(request):
    all_products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    selected_sort = request.GET.get('sort')
    selected_category = request.GET.get('category')

    # Filter by category
    query = all_products
    if selected_category:
        query = query.filter(category__category_name=selected_category)

    # Sort products
    if selected_sort:
        if selected_sort == 'newest':
            query = query.filter(newest_product=True).order_by('-created_at')
        elif selected_sort == 'priceAsc':
            query = query.order_by('price')
        elif selected_sort == 'priceDesc':
            query = query.order_by('-price')

    # Paginate
    if query.exists():
        page = request.GET.get('page', 1)
        paginator = Paginator(query, 20)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        except Exception as e:
            print(f"Pagination error: {e}")
            products = paginator.page(1)
    else:
        products = None

    # Extra sections for homepage
    trending_products = all_products.filter(newest_product=True)[:8]
    new_arrivals = all_products[:8]
    featured_categories = categories[:6]

    context = {
        'products': products,
        'categories': categories,
        'featured_categories': featured_categories,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'selected_category': selected_category,
        'selected_sort': selected_sort,
        'total_products': all_products.count(),
    }
    return render(request, 'home/index.html', context)


def product_search(request):
    query = request.GET.get('q', '')

    if query:
        # Search for products that contain the query string in their product_name field
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(
            product_name__istartswith=query))
    else:
        products = Product.objects.none()

    context = {'query': query, 'products': products}
    return render(request, 'home/search.html', context)


def contact(request):
    context = {"form_id": "xgvvlrvn"}
    return render(request, 'home/contact.html', context)


def about(request):
    return render(request, 'home/about.html')


def terms_and_conditions(request):
    return render(request, 'home/terms_and_conditions.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')
