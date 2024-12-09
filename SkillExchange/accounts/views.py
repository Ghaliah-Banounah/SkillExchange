from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.db import transaction, IntegrityError
from skills.models import Skill

# Create new account View
def register_view(request:HttpRequest):
    
    skills = Skill.objects.all()
    profile_form = ProfileForm()

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(first_name=request.POST['fname'], last_name=request.POST['lname'], username=request.POST['username'].lower(), email=request.POST['email'], password=request.POST['password'])
                new_user.save()

                # Create profile
                new_profile = Profile(user=new_user)
                profile_form = ProfileForm(request.POST, request.FILES, instance=new_profile)
                if profile_form.is_valid():
                    profile_form.save()
                else:
                    raise Exception(profile_form.errors.as_data())

            messages.success(request, "Register successfull.", "alert-success")   
            return redirect('accounts:login_view')
            
        except IntegrityError:
            messages.warning(request, "The username is already taken. Please choose another one.", "alert-warning")
        except Exception as e:
            messages.error(request, f"{e} Register failed. Try again", "alert-danger")    

    return render(request, 'accounts/register.html', {'skills': skills})

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
    
    skills = Skill.objects.all()
    if request.method == 'POST':
        try:
            user:User = request.user
            profile:Profile = user.profile
            with transaction.atomic():
                # Update user instance
                user.first_name=request.POST['fname']
                user.last_name=request.POST['lname']
                user.email=request.POST['email']
                user.save()
                
                # Update user profile
                profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
                if profile_form.is_valid():
                    profile_form.save()
                else:
                    raise Exception(profile_form.errors.as_data())

            messages.success(request, "Profile updated successfully.", "alert-success")
            return redirect('accounts:profile_view', user.username)
        
        except Exception as e:
            messages.error(request, f"{e} Profile wasn't updated.", "alert-danger")

    return render(request, 'accounts/updateProfile.html', {'skills': skills})
