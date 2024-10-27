import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from catalog.models import Sneaker
from keranjang.models import CartItem, UserCart


def view_keranjang(request):
    item_added = request.session.get('item_added', False)
    request.session['item_added'] = False
    
    return render(request, 'keranjang.html', {'item_added': item_added})

@login_required(login_url='homepage:login')
def add_to_cart(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    user = request.user

    try:
        cart_item = get_object_or_404(CartItem, user=user, sneaker=sneaker)
        cart_item.quantity += 1
    except Http404:
        cart_item = CartItem (
            user = user,
            sneaker = sneaker,
            quantity = 1,
        )
        
    cart_item.save()

    request.session['item_added'] = True

    return redirect('keranjang:view_keranjang')

@login_required
def remove_from_cart(request, slug):
    keranjang = request.session.get('keranjang', {})

    if str(slug) in keranjang:
        del keranjang[str(slug)]

    request.session['keranjang'] = keranjang

    return redirect('keranjang:view_keranjang')


@login_required(login_url='login')
def checkout(request):
    keranjang = request.session.get('keranjang', {})
    if not keranjang:
        return redirect('keranjang:view_keranjang')

    if request.method == 'POST':
        # Proses checkout
        # ...
        return redirect('keranjang:payment_successful')
    else:
        item_keranjang = []
        total_harga = 0
        for slug, kuantitas in keranjang.items():
            sneaker = get_object_or_404(Sneaker, slug=slug)
            item_keranjang.append({
                'sneaker': sneaker,
                'kuantitas': kuantitas,
                'total_harga': sneaker.price * kuantitas,
            })
            total_harga += sneaker.price * kuantitas
        return render(request, 'keranjang/checkout.html', {
            'item_keranjang': item_keranjang,
            'total_harga': total_harga,
        })

@login_required(login_url='login')
def payment_successful(request):
    # Tampilkan halaman konfirmasi tanpa riwayat pembelian
    return render(request, 'checkout.html')

def update_quantity(request, slug):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and int(quantity) > 0:
            keranjang = request.session.get('keranjang', {})
            keranjang[str(slug)] = int(quantity)
            request.session['keranjang'] = keranjang
            messages.success(request, 'Kuantitas berhasil diperbarui.')
        else:
            messages.error(request, 'Masukkan jumlah yang valid.')
    return redirect('keranjang:view_keranjang')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def update_quantity_ajax(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        quantity = request.POST.get('quantity')

        if slug and quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    keranjang = request.session.get('keranjang', {})
                    keranjang[slug] = quantity
                    request.session['keranjang'] = keranjang

                    sneaker = get_object_or_404(Sneaker, slug=slug)
                    item_total_harga = sneaker.price * quantity

                    total_harga = 0
                    total_items = 0 
                    for slug, kuantitas in keranjang.items():
                        item_sneaker = get_object_or_404(Sneaker, slug=slug)
                        total_harga += item_sneaker.price * kuantitas
                        total_items += kuantitas  

                    return JsonResponse({
                        'item_total_harga': item_total_harga,
                        'total_harga': total_harga,
                        'total_items': total_items,
                    })
                else:
                    return JsonResponse({'error': 'Jumlah tidak valid'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Jumlah tidak valid'}, status=400)
        else:
            return JsonResponse({'error': 'Parameter hilang'}, status=400)
    else:
        return JsonResponse({'error': 'Metode permintaan tidak valid'}, status=405)


@csrf_exempt
def remove_from_cart_ajax(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        if slug:
            keranjang = request.session.get('keranjang', {})
            if slug in keranjang:
                del keranjang[slug]
                request.session['keranjang'] = keranjang

                total_harga = 0
                total_items = 0  
                for slug, kuantitas in keranjang.items():
                    item_sneaker = get_object_or_404(Sneaker, slug=slug)
                    total_harga += item_sneaker.price * kuantitas
                    total_items += kuantitas

                cart_empty = len(keranjang) == 0

                return JsonResponse({
                    'total_harga': total_harga,
                    'total_items': total_items,
                    'cart_empty': cart_empty,
                })
            else:
                return JsonResponse({'error': 'Item tidak ada di keranjang'}, status=404)
        else:
            return JsonResponse({'error': 'Item ID hilang'}, status=400)
    else:
        return JsonResponse({'error': 'Metode permintaan tidak valid'}, status=405)
    
def get_user_cart(request):
    user_cart = UserCart.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", user_cart), content_type="application/json")

def get_sneaker(request, id):
    sneaker = Sneaker.objects.filter(id=id)
    return HttpResponse(serializers.serialize("json", sneaker), content_type="application/json")
    
def show_xml(request):
    data = CartItem.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = CartItem.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, review_id):
    data = CartItem.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, review_id):
    data = CartItem.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")