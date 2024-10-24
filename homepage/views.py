from django.shortcuts import render

# Create your views here.
def view_homepage(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "homepage.html", context)