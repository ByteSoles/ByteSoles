from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def show_homepage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage:show_homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
        
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'homepage.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('homepage:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('homepage:show_homepage'))
    response.delete_cookie('last_login')
    return response

# Create your views here.
def view_homepage(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "homepage.html", context)
    return render(request, "homepage.html", context)
