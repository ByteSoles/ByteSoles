import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from review.models import Review, Rating
from review.forms import ReviewForm
from catalog.models import Sneaker
from keranjang.models import CartItem 
from django.contrib.auth.models import User
from django.db import transaction

def show_reviews(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug) 

    if request.user.is_authenticated:
        user = request.user 
    else:
        user = None      

    context = {
        'sneaker': sneaker,
        'user': user
    }    
    return render(request, 'reviews.html', context)

@csrf_exempt
@require_POST
@login_required
def add_review_ajax(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    review_description = request.POST.get("review_description")
    score = request.POST.get("score")

    new_review = Review (
        user = request.user,
        username = request.user.username,
        sneaker = sneaker,
        review_description = review_description, 
        score = score,
    )
    new_review.save()

    try:
        rating = get_object_or_404(Rating, sneaker=sneaker)
        rating.total_score += int(score)
        rating.review_count += 1
        rating.rating = rating.total_score / rating.review_count
    except Http404:
        rating = Rating (
            sneaker = sneaker,
            total_score = score,
            review_count = 1,
            rating = score
        )
    
    rating.save()

    return HttpResponse(b"CREATED", status=200)

@csrf_exempt
def add_review_ajax_flutter(request):
    try:
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        sneaker_id = request.POST.get("sneaker_id")
        review_description = request.POST.get("review_description")
        score = request.POST.get("score")

        user = User.objects.get(id=user_id)
        sneaker = Sneaker.objects.get(id=sneaker_id)

        # Validate required fields
        if not all([user_id, username, sneaker_id, review_description, score]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)

        new_review = Review(
            user=user,
            username=username,
            sneaker=sneaker,
            review_description=review_description,
            score=score,
        )
        new_review.save()

        try:
            rating = get_object_or_404(Rating, sneaker=sneaker)
            rating.total_score += int(score)
            rating.review_count += 1
            rating.rating = rating.total_score / rating.review_count
        except Http404:
            rating = Rating(
                sneaker=sneaker,
                total_score=score,
                review_count=1,
                rating=score
            )
        
        rating.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Review added successfully'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_POST
@login_required
def edit_review_ajax(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    review_description = request.POST.get("review_description")
    score = request.POST.get("score")

    review = get_object_or_404(Review, user=request.user, sneaker=sneaker)
    rating = get_object_or_404(Rating, sneaker=sneaker)
    review.review_description = review_description

    rating.total_score -= review.score
    review.score = int(score)
    rating.total_score += review.score
    rating.rating = rating.total_score / rating.review_count

    review.save()
    rating.save()

    return HttpResponse(b"UPDATED", status=200)

@login_required
def delete_review(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    review = get_object_or_404(Review, user=request.user, sneaker=sneaker)
    rating = get_object_or_404(Rating, sneaker=sneaker)

    rating.total_score -= review.score
    rating.rating = rating.total_score / rating.review_count
    rating.review_count -= 1

    review.delete()
    rating.save()

    return HttpResponse(b"DELETED", status=200)

@csrf_exempt
def delete_review_flutter(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)

    try:
        user_id = request.POST.get("user_id")
        sneaker_id = request.POST.get("sneaker_id")

        # Validate required fields
        if not all([user_id, sneaker_id]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)

        try:
            user = User.objects.get(id=user_id)
            sneaker = Sneaker.objects.get(id=sneaker_id)
        except (User.DoesNotExist, Sneaker.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'User or Sneaker not found'
            }, status=404)
        
        try:
            rating = get_object_or_404(Rating, sneaker=sneaker)
            review = get_object_or_404(Review, user=user, sneaker=sneaker)

            rating.total_score -= review.score
            rating.review_count -= 1
            if rating.review_count > 0:
                rating.rating = rating.total_score / rating.review_count
            else:
                rating.rating = 0
                rating.total_score = 0

            review.delete()
            rating.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Review deleted successfully'
            })
        except Review.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Review not found'
            }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def get_rating(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)

    try:
        rating = get_object_or_404(Rating, sneaker=sneaker)
    except Http404:
        return HttpResponse(0.0)

    return HttpResponse(rating.rating)

def get_review_by_username(request, sneaker, username):
    review = get_object_or_404(Review, sneaker=sneaker, username=username)
    return HttpResponse(serializers.serialize("json", [review]), content_type="application/json")

def show_xml(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    data = Review.objects.filter(sneaker=sneaker)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request, slug):
    sneaker = get_object_or_404(Sneaker, slug=slug)
    data = Review.objects.filter(sneaker=sneaker)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")