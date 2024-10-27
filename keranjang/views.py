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
from django.http import JsonResponse


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
@login_required
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

    return HttpResponse(b"UPDATED", status=201)

@csrf_exempt
@require_POST
@login_required
def remove_from_cart_ajax(request):
    sneaker = request.POST.get('sneaker')
    cart = get_object_or_404(UserCart, user=request.user)
    cart_item = get_object_or_404(CartItem, user=request.user, sneaker=sneaker)

    cart.total_items -= cart_item.quantity
    cart.total_price -= cart_item.total_price

    cart.save()
    cart_item.delete()

    return HttpResponse(b"DELETED", status=201)
    
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


