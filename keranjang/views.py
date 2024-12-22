import datetime
from django.contrib.auth.models import User  
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
from django.http import JsonResponse
from django.contrib.auth.models import User  



def view_keranjang(request):
    item_added = request.session.get('item_added', False)
    request.session['item_added'] = False
    context = {
        'item_added': item_added,
    }
    return render(request, 'keranjang.html', context)

@login_required(login_url='homepage:login')
def add_to_cart(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    user = request.user
    cart = get_object_or_404(UserCart, user=request.user)

    try:
        cart_item = get_object_or_404(CartItem, user=user, sneaker=sneaker)
        cart_item.quantity += 1
        cart_item.total_price += sneaker.price
    except Http404:
        cart_item = CartItem (
            user = user,
            sneaker = sneaker,
            sneaker_name = sneaker.name,
            sneaker_price = sneaker.price,
            sneaker_image = sneaker.image,
            quantity = 1,
            total_price = sneaker.price
        )
    cart.total_items += 1
    cart.total_price += sneaker.price

    cart.save()
    cart_item.save()

    request.session['item_added'] = True

    return redirect('keranjang:view_keranjang')

@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(UserCart, user=request.user)
    cart_item = CartItem.objects.filter(user=request.user)
    items = []

    for item in cart_item:
        sneaker = get_object_or_404(Sneaker, name=item.sneaker)
        items.append({
            'sneaker': sneaker,
            'quantity': item.quantity,
            'total_price': item.total_price,
        })
    
    data = {
        'items': items,
        'total_price': cart.total_price,
    }

    return render(request, 'keranjang/checkout.html', data)

@csrf_exempt
@require_POST
@login_required(login_url='login')
def update_quantity_ajax(request):
    sneaker = request.POST.get('sneaker')
    quantity = request.POST.get('quantity')
    cart = get_object_or_404(UserCart, user=request.user)
    cart_item = get_object_or_404(CartItem, user=request.user, sneaker=sneaker)

    cart.total_items -= cart_item.quantity
    cart_item.quantity = int(quantity)
    cart.total_items += cart_item.quantity

    cart.total_price -= cart_item.total_price
    cart_item.total_price = cart_item.quantity * cart_item.sneaker_price
    cart.total_price += cart_item.total_price

    cart.save()
    cart_item.save()

    # Mengirimkan respons JSON
    return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})


from django.http import JsonResponse

@csrf_exempt
@require_POST
@login_required
def remove_from_cart_ajax(request):
    # print("Endpoint remove_from_cart_ajax terpanggil") 
    sneaker = request.POST.get('sneaker')
    # print("Sneaker ID yang diterima:", sneaker)  

    try:
        cart = get_object_or_404(UserCart, user=request.user)
        cart_item = get_object_or_404(CartItem, user=request.user, sneaker=sneaker)

        cart.total_items -= cart_item.quantity
        cart.total_price -= cart_item.total_price

        cart.save()
        cart_item.delete()

        return JsonResponse({'status': 'success', 'message': 'Item removed successfully'})
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@csrf_exempt
@require_POST
# @login_required(login_url='homepage:login')
def remove_from_cart_ajax_flutter(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        sneaker_id = request.POST.get('sneaker')
        sneaker_name = request.POST.get('sneaker_name')
        sneaker_price = request.POST.get('sneaker_price')
        sneaker_image = request.POST.get('sneaker_image')
        quantity = request.POST.get('quantity')
        purchase_date = request.POST.get('purchase_date')
        total_price = request.POST.get('total_price')
        
        # Cari dan hapus item berdasarkan kombinasi field
        try:
            cart_item = CartItem.objects.get(
                user_id=user_id,
                sneaker_id=sneaker_id,
                sneaker_name=sneaker_name,
                sneaker_price=sneaker_price,
                sneaker_image=sneaker_image,
                quantity=quantity,
                purchase_date=purchase_date,
                total_price=total_price,
            )
            cart_item.delete()
            return JsonResponse({'status': 'success'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item tidak ditemukan'}, status=404)

@csrf_exempt
@require_POST
def add_to_cart_flutter(request):
    if request.method == 'POST':
        try:
            print("Received data:", request.POST)
            
            user_id = request.POST.get('user')
            sneaker_id = request.POST.get('sneaker')
            
            print(f"Processing: User ID: {user_id}, Sneaker ID: {sneaker_id}")

            if not user_id or not sneaker_id:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing data: user_id={user_id}, sneaker_id={sneaker_id}'
                }, status=400)

            try:
                user = User.objects.get(id=user_id)
                sneaker = Sneaker.objects.get(id=sneaker_id)
            except User.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'User with id {user_id} not found'
                }, status=404)
            except Sneaker.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Sneaker with id {sneaker_id} not found'
                }, status=404)

            cart, _ = UserCart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                sneaker=sneaker,
                defaults={
                    'sneaker_name': sneaker.name,
                    'sneaker_price': sneaker.price,
                    'sneaker_image': sneaker.image,
                    'quantity': 0,
                    'total_price': 0
                }
            )

            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * sneaker.price
            cart_item.save()

            cart.total_items = CartItem.objects.filter(user=user).count()
            cart.total_price = sum(item.total_price for item in CartItem.objects.filter(user=user))
            cart.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Item berhasil ditambahkan ke keranjang'
            })
            
        except Exception as e:
            print(f"Error in add_to_cart_flutter: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        
def get_user_cart(request):
    user_cart = UserCart.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", user_cart), content_type="application/json")

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