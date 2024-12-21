from django.shortcuts import render, get_object_or_404
from catalog.models import Sneaker
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from detail_product.models import Product

def view_catalog(request):
    sneakers = Sneaker.objects.all().values()
    context = {
        'sneakers': sneakers,
        'name': request.user.username,
    }
    return render(request, "view_catalog.html", context)

def get_product_json(request):
    product_item = Sneaker.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))


def get_filtered_products(request):
    min_price = request.GET.get('min_price', 50) 
    max_price = request.GET.get('max_price', 500)  
    brand = request.GET.get('brand','all') 


    products = Sneaker.objects.filter(price__gte=min_price, price__lte=max_price)
    if brand != 'all':
        products = products.filter(brand=brand)


    product_list = [{
        'name': product.name,
        'brand': product.brand,
        'price': product.price,
        'image': product.image if product.image else '',
        'slug': product.slug
    } for product in products]

    return JsonResponse(product_list, safe=False)


def product_detail(request, slug):
    product = get_object_or_404(Sneaker, slug=slug)
    return render(request, 'detail_product/detail_product.html', {'product': product})
    return render(request, 'detail_product.html', context)

def get_product_by_id(request, id):
    product = get_object_or_404(Product, id=id)
    product_data = {
        "model": "detail_product.product",
        "pk": product.id,
        "fields": {
            "name": product.name,
            "brand": product.brand,
            "price":product.price,
            "description": product.description,
            "release_date": product.release_date,
            "slug" : product.slug,
            "image": product.image if product.image else '',
        }
    }
    return JsonResponse(product_data)



