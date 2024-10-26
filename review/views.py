import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from review.models import Review
from review.forms import ReviewForm
from catalog.models import Sneaker

def show_reviews(request, sneaker_name):
    sneaker = get_object_or_404(Sneaker, name=sneaker_name)

    if request.user.is_authenticated:
        user = request.user 
    else:
        user = None

    context = {
        'sneaker_name': sneaker,
        'image': sneaker.image,
        'user': user
    }    
    return render(request, 'reviews.html', context)

@csrf_exempt
@require_POST
@login_required
def add_review_ajax(request, sneaker_name):
    sneaker = get_object_or_404(Sneaker, name=sneaker_name)
    review_description = request.POST.get("review_description")
    score = request.POST.get("score")

    new_review = Review(
        user=request.user,
        username=request.user.username,
        sneaker=sneaker,
        review_description=review_description, 
        score=score,
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)

def show_xml(request, sneaker_name):
    sneaker =get_object_or_404(Sneaker, name=sneaker_name)
    data = Review.objects.filter(sneaker=sneaker)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request, sneaker_name):
    sneaker =get_object_or_404(Sneaker, name=sneaker_name)
    data = Review.objects.filter(sneaker=sneaker)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")