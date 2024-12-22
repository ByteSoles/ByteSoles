from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from catalog.models import Sneaker
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

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

@csrf_exempt
def remove_from_wishlist(request, product_id):
    try:
        if request.method == 'POST':
            # Parse data yang diterima
            user_id = request.POST.get('user')
            sneaker_id = request.POST.get('sneaker')
            
            # Jika data tidak ada di POST, coba ambil dari body
            if not user_id or not sneaker_id:
                try:
                    data = json.loads(request.body)
                    user_id = data.get('user')
                    sneaker_id = data.get('sneaker')
                except json.JSONDecodeError:
                    pass

            # Validasi data
            if not user_id or not sneaker_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required data'
                }, status=400)

            # Hapus item dari wishlist
            try:
                user = User.objects.get(id=int(user_id))
                wishlist_item = Wishlist.objects.get(
                    user=user,
                    product_id=product_id
                )
                wishlist_item.delete()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Item berhasil dihapus'
                })
            except (User.DoesNotExist, Wishlist.DoesNotExist):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Item tidak ditemukan'
                }, status=404)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

@login_required
def get_wishlist_json(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    data = [{
        'id': item.product.id,
        'name': item.product.name,
        'brand': item.product.brand,
        'price': item.product.price,
        'image': item.product.image if item.product.image else '',
        'slug': item.product.slug
    } for item in wishlist_items]
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_to_wishlist_flutter(request):
    if request.method == 'POST':
        try:
            # Coba ambil data dari request.POST terlebih dahulu
            user_id = request.POST.get('user')
            sneaker_id = request.POST.get('sneaker')
            
            # Jika tidak ada di POST, coba ambil dari body
            if not user_id or not sneaker_id:
                try:
                    data = json.loads(request.body)
                    user_id = data.get('user')
                    sneaker_id = data.get('sneaker')
                except json.JSONDecodeError:
                    pass

            print(f"Processing: User ID: {user_id}, Sneaker ID: {sneaker_id}")

            if not user_id or not sneaker_id:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing data: user_id={user_id}, sneaker_id={sneaker_id}'
                }, status=400)

            try:
                user = User.objects.get(id=int(user_id))
                sneaker = Sneaker.objects.get(id=int(sneaker_id))
            except (User.DoesNotExist, Sneaker.DoesNotExist, ValueError):
                return JsonResponse({
                    'status': 'error',
                    'message': 'User or Sneaker not found'
                }, status=404)
            
            # Cek apakah item sudah ada di wishlist
            existing_item = Wishlist.objects.filter(user=user, product=sneaker).first()
            if existing_item:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Produk sudah ada di wishlist'
                })
            
            # Buat item wishlist baru
            Wishlist.objects.create(user=user, product=sneaker)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Produk berhasil ditambahkan ke wishlist'
            })
            
        except Exception as e:
            print(f"Error in add_to_wishlist_flutter: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
