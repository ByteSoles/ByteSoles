from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Product, Comment
from .forms import CommentForm
import json
from django.contrib.auth.decorators import login_required

def get_product_by_id(request, id):
    product = get_object_or_404(Product, id=id)
    product_data = {
        "model": "detail_product.product",
        "pk": product.id,
        "fields": {
            "name": product.name,
            "brand": product.brand,
            "price": str(product.price),  # Convert Decimal to string for JSON serialization
            "description": product.description,
            "image": product.image.url if product.image else '',  # Use .url for ImageField
            "slug" : product.slug,
        }
    }
    return JsonResponse(product_data)




@csrf_exempt  # Since we're handling this as an API endpoint
def add_comment(request, product_slug):
    print("=== Debug Info ===")
    print(f"Is user authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")
    print(f"Session ID: {request.session.session_key}")
    print(f"Headers: {request.headers}")
    print(f"Cookies: {request.COOKIES}")
    print("=================")
    # Check authentication manually
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'User not authenticated'
        }, status=401)  # Return 401 Unauthorized instead of redirecting

    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)

    try:
        # Add debug prints
        print(f"User attempting to comment: {request.user.username}")
        print(f"Product slug: {product_slug}")
        print(f"Request data: {request.POST}")

        product = get_object_or_404(Product, slug=product_slug)
        content = request.POST.get('content')

        if not content:
            return JsonResponse({
                'status': 'error',
                'message': 'Comment content is required'
            }, status=400)

        comment = Comment.objects.create(
            product=product,
            user=request.user,
            content=content
        )

        return JsonResponse({
            'status': 'success',
            'comment': {
                'user': request.user.username,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            }
        })

    except Exception as e:
        print(f"Error creating comment: {str(e)}")  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_comments(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    comments = product.comments.all().values('user', 'content', 'created_at')
    return JsonResponse(list(comments), safe=False)


def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    print(f"Fetched product: {product.name} with slug: {product.slug}")

    # Track recently viewed products in the session
    recent_products = request.session.get('recently_viewed', [])
    if product.id not in recent_products:
        recent_products.append(product.id)
        if len(recent_products) > 5:
            recent_products.pop(0)  # Keep only the last 5 items
    request.session['recently_viewed'] = recent_products

    # Fetch recently viewed products to display
    recently_viewed = Product.objects.filter(id__in=recent_products).exclude(id=product.id)

    context = {
        'product': product,
        'recently_viewed': recently_viewed,
    }
    return render(request, 'detail_product.html', context)
def get_recently_viewed(request):
    recent_ids = request.session.get('recently_viewed', [])
    recent_products = Product.objects.filter(id__in=recent_ids)
    
    data = [
        {
            'name': product.name,
            'brand': product.brand,
            'price': product.price,
            'image': product.image,
            'slug': product.slug,
        }
        for product in recent_products
    ]
    
    return JsonResponse(data, safe=False)
