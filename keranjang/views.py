from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Sneaker
from django.contrib import messages


def view_keranjang(request):
    keranjang = request.session.get('keranjang', {})
    item_keranjang = []
    total_harga = 0

    for item_id, kuantitas in keranjang.items():
        sneaker = get_object_or_404(Sneaker, id=item_id)
        item_keranjang.append({
            'sneaker': sneaker,
            'kuantitas': kuantitas,
            'total_harga': sneaker.price * kuantitas,
        })
        total_harga += sneaker.price * kuantitas

    item_added = request.session.get('item_added', False)
    request.session['item_added'] = False

    return render(request, 'keranjang.html', {
        'item_keranjang': item_keranjang,
        'total_harga': total_harga,
        'item_added': item_added,
    })

@login_required(login_url='login')
def add_to_cart(request, item_id):
    sneaker = get_object_or_404(Sneaker, id=item_id)
    keranjang = request.session.get('keranjang', {})

    if str(item_id) in keranjang:
        keranjang[str(item_id)] += 1
    else:
        keranjang[str(item_id)] = 1

    request.session['keranjang'] = keranjang
    request.session['item_added'] = True

    return redirect('keranjang:view_keranjang')

@login_required
def remove_from_cart(request, item_id):
    keranjang = request.session.get('keranjang', {})

    if str(item_id) in keranjang:
        del keranjang[str(item_id)]

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
        for item_id, kuantitas in keranjang.items():
            sneaker = get_object_or_404(Sneaker, id=item_id)
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

def update_quantity(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and int(quantity) > 0:
            keranjang = request.session.get('keranjang', {})
            keranjang[str(item_id)] = int(quantity)
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
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        if item_id and quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    keranjang = request.session.get('keranjang', {})
                    keranjang[item_id] = quantity
                    request.session['keranjang'] = keranjang

                    sneaker = get_object_or_404(Sneaker, id=item_id)
                    item_total_harga = sneaker.price * quantity

                    total_harga = 0
                    total_items = 0 
                    for id_item, kuantitas in keranjang.items():
                        item_sneaker = get_object_or_404(Sneaker, id=id_item)
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
        item_id = request.POST.get('item_id')
        if item_id:
            keranjang = request.session.get('keranjang', {})
            if item_id in keranjang:
                del keranjang[item_id]
                request.session['keranjang'] = keranjang

                total_harga = 0
                total_items = 0  
                for id_item, kuantitas in keranjang.items():
                    item_sneaker = get_object_or_404(Sneaker, id=id_item)
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


