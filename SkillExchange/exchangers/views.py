from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Exchanger, Request
from django.contrib.auth.models import User

# Display exchangers
def display_exchangers_view(request: HttpRequest):
    
    exchangers = User.objects.all()
    return render(request, 'exchangers/display_exchangers.html', {'exchangers': exchangers})

# Send request View
def send_request_view(request: HttpRequest, sender_id: int, receiver_id: int):
    try: 
                
        if not request.user.is_authenticated:
            messages.warning(request, "You must login to send a request", "alert-warning")
            return redirect("accounts:login_view") 

        receiver = User.objects.get(pk=receiver_id)
        sender = User.objects.get(pk=sender_id)

        if sender == request.user:
            messages.warning(request, "You cant send a request to yourself", "alert-warning")
            return redirect("accounts:login_view") 

        request_obj = Request.objects.filter(sender = sender, receiver = receiver).first()

        if not request_obj:
            if request.method == "POST":
                scheduled_at = request.POST.get("scheduled_at")
                new_request=Request(sender=sender, receiver=receiver, scheduled_at=scheduled_at)
                new_request.save()
        else:
            request_obj.delete()

        return redirect("accounts:profile_view", receiver.username)
    except Exception as e:
            print(e)
            return redirect("main:home_view")

# Reject request View
def reject_request_view(request: HttpRequest, sender_id: int, receiver_id: int):
    try:
        receiver=User.objects.get(pk=receiver_id)
        sender = User.objects.get(pk=sender_id)

        if not request.user.is_authenticated and sender != request.user:
            messages.warning(request, "Only the user who received the request can reject it.", "alert-warning")
            return redirect("accounts:login_view") 
        
        request_obj = Request.objects.get(sender=sender,receiver=receiver)
        request_obj.delete()
        return redirect("accounts:profile_view", receiver.username)
    
    except Exception as e:
            print(e)
            return redirect("main:home_view")

# New exchange View
def new_exchange_view(request: HttpRequest, user_id: int, exchanger_id: int):
    return render()

# New exchange View
def delete_exchange_view(request: HttpRequest, user_id: int, exchanger_id: int):
    return render()