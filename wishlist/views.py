from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from catalog.models import Sneaker

# Create your views here.

def product_list(request):
    products = Sneaker.objects.all()
    return render(request, 'wishlist/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Sneaker, pk=product_id)
    return render(request, 'wishlist/product_detail.html', {'product': product})

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Sneaker, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan ke wishlist'})
    return redirect('wishlist:wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('wishlist:wishlist')
