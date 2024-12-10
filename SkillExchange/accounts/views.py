from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.db import transaction, IntegrityError

# Create new account View
def register_view(request:HttpRequest):
 
    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(first_name=request.POST['fname'], last_name=request.POST['lname'], username=request.POST['username'].lower(), email=request.POST['email'], password=request.POST['password'])
                new_user.save()

                # Create profile
                profile = Profile(user=new_user, bio=request.POST['bio'], pfp=request.FILES.get('pfp', Profile.pfp.field.get_default()))
                profile.save()

            messages.success(request, "Register successfull.", "alert-success")   
            return redirect('accounts:login_view')
            
        except IntegrityError:
            messages.warning(request, "The username is already taken. Please choose another one.", "alert-warning")
        except Exception as e:
            messages.error(request, f"{e} Register failed. Try again", "alert-danger")    

    return render(request, 'accounts/register.html')

# Login to existing account View
def login_view(request:HttpRequest):

    if request.method == 'POST':
        # Check user credentials
        user = authenticate(request, username=request.POST["username"].lower(), password=request.POST["password"])
        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}.", "alert-success")
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, "Login failed. Your credentials are incorrect.", "alert-danger")   
    
    return render(request, 'accounts/login.html')

# Logout View
def logout_view(request:HttpRequest):
    
    logout(request)
    messages.success(request, "Logged out successfully.", "alert-success")
    return redirect(request.GET.get('next', '/'))
    
# Display profile View
def profile_view(request: HttpRequest, username: str):
    try:
        user = User.objects.get(username__iexact=username)
        if Profile.objects.filter(user=user).exists():
            profile: Profile = user.profile
        else:
            profile = Profile(user=user)
    except Exception as e:
        print(e)
        return render(request, '404.html')
    
    return render(request, 'accounts/profile.html', {'profile': profile})

# Display profile View
def update_profile_view(request: HttpRequest):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Login to update your account.", "alert-warning")
        return redirect('accounts:login_view')
    
    if request.method == 'POST':
        try:
            user:User = request.user
            profile:Profile = user.profile
            with transaction.atomic():
                # Update user instance
                user.first_name=request.POST['fname']
                user.last_name=request.POST['lname']
                user.username=request.POST['username']
                user.email=request.POST['email']
                user.save()
                
                # Update user profile
                profile.bio=request.POST['bio']
                profile.pfp=request.FILES.get('pfp', profile.pfp)
                profile.save()

            messages.success(request, "Profile updated successfully.", "alert-success")
            return redirect('accounts:profile_iew', user.username)
        
        except Exception as e:
            messages.error(request, f"Profile wasn't updated.", "alert-danger")

    return render(request, 'accounts/updateProfile.html')
