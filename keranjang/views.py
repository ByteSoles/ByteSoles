from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Sneaker
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import UserCart, PurchaseHistory
import json


def view_keranjang(request):
    keranjang = request.session.get('keranjang', {})
    item_keranjang = []
    total_harga = 0
    invalid_items = []

    for slug, kuantitas in keranjang.items():
        try:
            sneaker = Sneaker.objects.get(slug=slug)
            item_keranjang.append({
                'sneaker': sneaker,
                'kuantitas': kuantitas,
                'total_harga': sneaker.price * kuantitas,
            })
            total_harga += sneaker.price * kuantitas
        except Sneaker.DoesNotExist:
            invalid_items.append(slug)

    # Hapus item yang tidak valid dari keranjang
    for slug in invalid_items:
        del keranjang[slug]
    request.session['keranjang'] = keranjang

    item_added = request.session.get('item_added', False)
    request.session['item_added'] = False

    return render(request, 'keranjang.html', {
        'item_keranjang': item_keranjang,
        'total_harga': total_harga,
        'item_added': item_added,
    })


@login_required(login_url='login')
def add_to_cart(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    keranjang = request.session.get('keranjang', {})
    

    if str(slug) in keranjang:
        keranjang[str(slug)] += 1
    else:
        keranjang[str(slug)] = 1

    request.session['keranjang'] = keranjang
    request.session['item_added'] = True

    cartitem = PurchaseHistory (
        user = request.user,
        sneaker = sneaker,
        quantity = 1,
    )
    cartitem.save()
    return redirect('keranjang:view_keranjang')

@login_required(login_url='login')
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
    purchase_history = PurchaseHistory.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'checkout_success.html', {
        'purchase_history': purchase_history,
    })


def update_quantity(request, slug):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and int(quantity) > 0:
            keranjang = request.session.get('keranjang', {})
            keranjang[str(slug)] = int(quantity)
            request.session['keranjang'] = keranjang
            sneaker = get_object_or_404(Sneaker,slug=slug)
            cartitem = get_object_or_404(PurchaseHistory,sneaker=sneaker)
            cartitem.quantity = quantity
            cartitem.save()
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
    
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Muat keranjang dari database
                try:
                    user_cart = UserCart.objects.get(user=user)
                    cart_data = json.loads(user_cart.cart_data)
                    request.session['keranjang'] = cart_data
                except UserCart.DoesNotExist:
                    request.session['keranjang'] = {}
                return redirect('homepage:show_homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def custom_logout(request):
    # Simpan keranjang ke database sebelum logout
    cart_data = request.session.get('keranjang', {})
    if cart_data:
        cart_json = json.dumps(cart_data)
        user_cart, created = UserCart.objects.get_or_create(user=request.user)
        user_cart.cart_data = cart_json
        user_cart.save()
    logout(request)
    return redirect('homepage:show_homepage')