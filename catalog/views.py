from django.shortcuts import render
from catalog.models import Sneaker
from django.core import serializers
from django.http import HttpResponse, JsonResponse

# Create your views here.

def view_catalog(request):
    sneakers = Sneaker.objects.all().values()[:100]
    context = {
        'sneakers': sneakers,
        'name': request.user.username,
    }
    return render(request, "view_catalog.html", context)

def get_product_json(request):
    product_item = Sneaker.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))


def get_filtered_products(request):
    min_price = request.GET.get('min_price', 50)  # Default min price $50
    max_price = request.GET.get('max_price', 500)  # Default max price $500

    # Filter products by price
    products = Sneaker.objects.filter(price__gte=min_price, price__lte=max_price)

    # Serialize the products to JSON format
    product_list = [{
        'name': product.name,
        'brand': product.brand,
        'price': product.price,
        'image': product.image.url if product.image else '',  # Handle image URL
    } for product in products]

    return JsonResponse(product_list, safe=False)
