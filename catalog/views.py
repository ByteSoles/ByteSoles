from django.shortcuts import render
from catalog.models import Sneaker

# Create your views here.

def view_catalog(request):
    sneakers = Sneaker.objects.all().values()[:100]
    context = {
        'sneakers': sneakers,
        'name': request.user.username,
    }
    return render(request, "view_catalog.html", context)