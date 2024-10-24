import datetime
from django.shortcuts import render, redirect, reverse
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

def show_reviews(request):
    return render(request, 'reviews.html')

def add_review(request, id):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('homepage:show_homepage')

    context = {'form': form}
    return render(request, 'add_review.html', context)

def show_xml(request, sneaker_id):
    data = Review.objects.filter(sneaker=sneaker_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request, sneaker_id):
    data = Review.objects.filter(sneaker=sneaker_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")