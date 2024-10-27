# user_profile/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile
from .forms import UserProfileForm  # Import form yang baru dibuat

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        shoe_size = request.POST.get('shoe_size')
        shipping_address = request.POST.get('shipping_address', '').strip()

        # Validasi shoe_size
        if shoe_size:
            try:
                shoe_size = float(shoe_size)
                request.user.profile.shoe_size = shoe_size
            except ValueError:
                return render(request, 'user_profile/profile.html')
        else:
            return render(request, 'user_profile/profile.html')

        # Update user data
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.profile.shipping_address = shipping_address
        
        request.user.save()
        request.user.profile.save()
        
        messages.success(request, 'Profil berhasil diperbarui!')
        
    return render(request, 'user_profile/profile.html')

def update_personal_info(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.profile.shoe_size = request.POST.get('shoe_size')
            user.save()
            user.profile.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def update_shipping_info(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            user = request.user
            user.profile.shipping_address = request.POST.get('shipping_address')
            user.profile.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Shipping info updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            # Update personal info
            if 'first_name' in request.POST:
                request.user.first_name = request.POST.get('first_name')
                request.user.last_name = request.POST.get('last_name')
                request.user.email = request.POST.get('email')
                request.user.profile.shoe_size = request.POST.get('shoe_size')
                request.user.save()
                request.user.profile.save()
                message = "Informasi pribadi berhasil diperbarui"
            
            # Update shipping info
            elif 'shipping_address' in request.POST:
                request.user.profile.shipping_address = request.POST.get('shipping_address')
                request.user.profile.save()
                message = "Alamat pengiriman berhasil diperbarui"
            
            return JsonResponse({
                'status': 'success',
                'message': message
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
