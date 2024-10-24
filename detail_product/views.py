# In detail_product/views.py

from catalog.models import Sneaker
from django.shortcuts import render, get_object_or_404

def show_product(request, product_name):
    # Use filter to get the product by name (adjust as needed)
    product = get_object_or_404(Sneaker, name=product_name)
    context = {
        'product': product,
    }
    return render(request, "detail_product.html", context)

def nyoba(request):
    return render(request, "nyoba.html")
