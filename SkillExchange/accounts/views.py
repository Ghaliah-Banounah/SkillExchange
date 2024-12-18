from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, Review
from .forms import ProfileForm
from exchangers.models import Exchanger, Request
from django.db import transaction, IntegrityError
from skills.models import Skill
from django.db.models import Q
from datetime import datetime

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
    except Exception as e:
        print(e)
        return render(request, '404.html')
    
    if Profile.objects.filter(user=user).exists():
            profile: Profile = user.profile
    else:
        profile = Profile(user=user)

    # Get requests sent or received by the user
    if request.user.is_authenticated:
        is_requested = Request.objects.filter(sender=request.user, receiver=user, status='Pending').exists()   

        # Check if they already have a connection
        is_connected = Exchanger.objects.filter(
            (Q(user=request.user) & Q(exchanger=user)) |
            (Q(user=user) & Q(exchanger=request.user))).exists()
        
        sent_requests = Request.objects.filter(sender=user, status=Request.RequestStatus.PENDING)
        received_requests = Request.objects.filter(receiver=user, status=Request.RequestStatus.PENDING)
        # Profile user exchanges
        current_exchanges = Exchanger.objects.filter((Q(user=user) | Q(exchanger=user)) & Q(end_date__gte=datetime.now()))
        # Current logged in user exchanges
        my_exchanges = Exchanger.objects.filter((Q(user=request.user) | Q(exchanger=request.user)) & Q(end_date__gte=datetime.now()))
        prev_exchanges = Exchanger.objects.filter((Q(user=user) | Q(exchanger=user)) & Q(end_date__lte=datetime.now()))

    else:
        sent_requests = []
        received_requests = []
        current_exchanges = []
        my_exchanges = []
        prev_exchanges = []
        is_requested = False
        is_connected = False
    
    return render(request, 'accounts/profile.html', {'profile': profile, 'is_connected': is_connected, 'is_requested': is_requested,
                   'sent_requests': sent_requests, 'received_requests': received_requests, 'current_exchanges': current_exchanges, 'prev_exchanges': prev_exchanges, 
                    'my_exchanges': my_exchanges, 'rating': reversed(Review.RatingChoices.choices)})

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

# Add review View
def add_review_view(request: HttpRequest, exchanger_id: int):
    if not (request.user.is_authenticated and Exchanger.objects.filter(Q(user=request.user) | Q(exchanger=request.user)).exists()):
        messages.error(request, "You can't add a review unless you have a previous exchange with this user." ,"alert-danger")
        return redirect("accounts:login_view")

    if request.method == "POST":
        try:
            exchanger = User.objects.get(pk=exchanger_id)
            new_review = Review(rating=request.POST['rating'], comment=request.POST['comment'], exchanger=exchanger, user=request.user)
            new_review.save()
            messages.success(request, "Review was added successfully.", "alert-success")

        except Exception as e:
            messages.error(request, "Something went wrong, couldn't add review", "alert-danger")

    return redirect("accounts:profile_view", exchanger.username)

# Delete review View
def delete_review_view(request: HttpRequest, review_id: int):
    if not ( request.user.is_staff and request.user.has_perm("accounts.delete_review")) and review.user != request.user:
        messages.warning(request, "You can't delete this review","alert-warning")
    else:
        try:
            review = Review.objects.get(pk=review_id)
        except Exception as e:
            return render(request, '404.html')        
        try:
            profile_username = review.exchanger.username
            review.delete()
            messages.success(request, "Review was deleted successfully", "alert-success")

        except Exception as e:
            messages.error(request, "Something went wrong, couldn't delete review", "alert-danger")
    
    return redirect("accounts:profile_view", profile_username)
