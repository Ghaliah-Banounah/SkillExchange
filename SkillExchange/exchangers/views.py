from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Exchanger, Request
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from skills.models import Skill

# Display exchangers
def display_exchangers_view(request: HttpRequest):

    search_query = request.GET.get('search', '')
    if search_query:
        exchangers = User.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    else:
        exchangers = User.objects.all()

    paginator = Paginator(exchangers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'exchangers/display_exchangers.html', {'exchangers': page_obj})

# Send request View
def send_request_view(request: HttpRequest, sender_id: int, receiver_id: int):
    try: 
                
        if not request.user.is_authenticated:
            messages.warning(request, "You must login to send a request", "alert-warning")
            return redirect("accounts:login_view") 
        
        # Account owner is the receiver
        receiver = User.objects.get(pk=receiver_id)
        # Logged in user is the sender
        sender = User.objects.get(pk=sender_id)

        if receiver == request.user:
            messages.warning(request, "You can't send a request to yourself", "alert-warning")
            return redirect("accounts:profile_view", receiver.username) 

        request_obj = Request.objects.filter(sender=sender, receiver=receiver).first()

        if not request_obj:
            if request.method == "POST":
                scheduled_at = request.POST["scheduled_at"].split(' - ')
                start_date = scheduled_at[0]
                end_date = scheduled_at[1]
                skill = Skill.objects.get(pk=request.POST["skill_to_exchange"])
                new_request=Request(sender=sender, receiver=receiver, start_date=start_date, end_date=end_date, skill_to_exchange=skill)
                new_request.save()
                messages.info(request, "Request sent.", "alert-primary")
        else:
            request_obj.delete()
            messages.info(request, "Request cancelled.", "alert-primary")

        return redirect("accounts:profile_view", receiver.username)
    except Exception as e:
            messages.error(request, f"Request couldn't be sent. {e}", "alert-danger")
            return redirect("accounts:profile_view", receiver.username)

# Reject request View
def reject_request_view(request: HttpRequest, sender_id: int, receiver_id: int):
    try:
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)

        if not request.user.is_authenticated and receiver != request.user:
            messages.warning(request, "Only the user who received the request can reject it.", "alert-warning")
            return redirect("accounts:profile_view", receiver.username)
        
        request_obj = Request.objects.get(sender=sender, receiver=receiver)
        request_obj.delete()
        messages.info(request, "Request rejected.", "alert-primary")

        return redirect("accounts:profile_view", receiver.username)
    
    except Exception as e:
            print(e)
            return redirect("main:home_view")

# New exchange View
def new_exchange_view(request: HttpRequest, user_id: int, exchanger_id: int):

    if not request.user.is_authenticated:
        messages.warning(request,"Login to accept requests.","alert-warning")
        return redirect("accounts:login_view") 
    
    try:
        # Logged in user
        user = User.objects.get(pk=user_id)
        # The user to exchange with 
        exchanger = User.objects.get(pk=exchanger_id)
        if request.user == user:
            if request.method == 'POST':
                with transaction.atomic():
                    request_obj = Request.objects.get(sender=exchanger_id, receiver=user_id)
                    request_obj.status = Request.RequestStatus.ACCEPTED
                    request_obj.save()
                    
                    exchange = Exchanger(user=user, exchanger=exchanger, start_date=request_obj.start_date, end_date=request_obj.end_date)
                    exchange.save()

        return redirect("accounts:profile_view", user.username)

    except Exception as e:
        print(e)
        return redirect("main:home_view")

# Delete exchange View
def delete_exchange_view(request: HttpRequest, user_id: int, exchanger_id: int):
    if not request.user.is_authenticated:
        messages.warning(request,"Login to reject requests.","alert-warning")
        return redirect("accounts:login_view") 
      
    try:
        # Logged in user
        user = User.objects.get(pk=user_id)
        # The user to exchange with 
        exchanger = User.objects.get(pk=exchanger_id)
        if request.user == user:
            with transaction.atomic():
                request_obj = Request.objects.get(sender=exchanger_id, receiver=user_id)
                request_obj.delete()

                exchange_obj = Exchanger.objects.get(user=user, exchanger=exchanger)
                exchange_obj.delete()

        return redirect("accounts:profile_view", user.username)

    except Exception as e:
        print(e)
        return redirect("main:home_view")