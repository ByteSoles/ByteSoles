from catalog.models import Sneaker
from django.shortcuts import render, get_object_or_404

def show_product(request, product_name):
    product = get_object_or_404(Sneaker, name=product_name)
    
    # Track recently viewed products in the session
    recent_products = request.session.get('recently_viewed', [])
    
    # Remove the product if it’s already in the list, then add it to the front
    if product.id in recent_products:
        recent_products.remove(product.id)
    recent_products.insert(0, product.id)
    
    # Keep only the last 5 items in recently viewed
    recent_products = recent_products[:5]
    request.session['recently_viewed'] = recent_products
    
    # Retrieve the recently viewed products from the database
    recent_products_qs = Sneaker.objects.filter(id__in=recent_products)
    
    # Sort the queryset based on the recent_products order
    recent_products_qs = sorted(recent_products_qs, key=lambda x: recent_products.index(x.id))
    print("Recent Products QuerySet:", recent_products_qs)
    print("Number of recent products:", recent_products_qs.count())
    
    context = {
        'product': product,
        'recent_products': recent_products_qs,
    }
    return render(request, "detail_product.html", context)
