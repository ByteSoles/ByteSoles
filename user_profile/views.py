from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile
from .forms import UserProfileForm 
from django.views.decorators.csrf import csrf_exempt

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

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            data = request.POST
            
            # Update user fields
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            
            # Update profile fields
            shipping_address = data.get('shipping_address', '')
            user.profile.shipping_address = shipping_address if shipping_address else '-'
            
            if 'shoe_size' in data:
                try:
                    shoe_size = float(data.get('shoe_size'))
                    user.profile.shoe_size = shoe_size
                except (ValueError, TypeError):
                    pass
            
            # Save both user and profile
            user.save()
            user.profile.save()
            
            print(f"Updated shipping_address: {user.profile.shipping_address}")  # Debug print
            
            return JsonResponse({
                'status': 'success',
                'message': 'Profil berhasil diperbarui'
            })
            
        except Exception as e:
            print(f'Error updating profile: {e}')
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@login_required
@csrf_exempt
def get_profile(request):
    if request.method == 'GET':
        try:
            user = request.user
            return JsonResponse({
                'status': 'success',
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'shoe_size': user.profile.shoe_size,
                'shipping_address': user.profile.shipping_address,
                'profile_picture': request.build_absolute_uri(user.profile.profile_picture.url) if user.profile.profile_picture else None
            })
        except Exception as e:
            print(f'Error getting profile: {e}')
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@login_required
@csrf_exempt
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            user = request.user
            user.profile.profile_picture = request.FILES['profile_picture']
            user.profile.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Foto profil berhasil diperbarui'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)

@login_required
@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Akun berhasil dihapus'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)