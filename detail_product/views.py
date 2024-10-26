# detail_product/views.py
from catalog.models import Sneaker
from django.shortcuts import render, get_object_or_404

def show_product(request, product_name):
    product = get_object_or_404(Sneaker, name=product_name)
    
    # Track recently viewed products in the session
    recent_products = request.session.get('recently_viewed', [])
    
    if product.id not in recent_products:
        recent_products.append(product.id)
        if len(recent_products) > 5:
            recent_products.pop(0)  # Keep only the last 5 items

    request.session['recently_viewed'] = recent_products
    recent_products_qs = Sneaker.objects.filter(id__in=recent_products)
    
    context = {
        'product': product,
        'recent_products': recent_products_qs,
    }
    return render(request, "detail_product.html", context)
