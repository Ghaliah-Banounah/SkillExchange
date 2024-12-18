from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Exchanger, Request
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.db import transaction
from skills.models import Skill
from datetime import datetime

# Display exchangers View
def display_exchangers_view(request: HttpRequest):

    search_query = request.GET.get('search', '')
    if search_query:
        exchangers = User.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    else:
        exchangers = User.objects.all()

    # Calculate average reviews per exchanger and assigining them to temp field
    exchangers = exchangers.annotate(average_rating=Avg("reviews__rating"))

    # Filtering by rating
    if 'rating' in request.GET and request.GET['rating'] == "highest":
        exchangers = exchangers.order_by('-average_rating')
    elif 'rating' in request.GET and request.GET['rating'] == "lowest":
        exchangers = exchangers.order_by('average_rating')

    # Filtering by join date
    if 'join_date' in request.GET and request.GET['join_date'] == "latest":
        exchangers = exchangers.order_by('-date_joined')
    elif 'join_date' in request.GET and request.GET['join_date'] == "oldest":
        exchangers = exchangers.order_by('date_joined')

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

        return redirect(request.GET.get('next', '/'))
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
            messages.error(request, "Something went wrong, couldn't reject request.", "alert-danger")
            return redirect("accounts:profile_view", receiver.username)

# New exchange View
def new_exchange_view(request: HttpRequest, sender_id: int, receiver_id: int):

    if not request.user.is_authenticated:
        messages.warning(request,"Login to accept requests.","alert-warning")
        return redirect("accounts:login_view") 
    
    try:
        # Receiver
        user = User.objects.get(pk=receiver_id)
        # Sender 
        exchanger = User.objects.get(pk=sender_id)
        
        if len(Exchanger.objects.filter((Q(user=user) | Q(exchanger=user)) & Q(status='Ongoing'))) == 3 or len(Exchanger.objects.filter((Q(user=request.user) | Q(exchanger=user)) & Q(status='Ongoing'))) == 3:
            messages.warning(request,"Exchange limit has been reached, subscribe to add more.","alert-warning")
            return redirect("accounts:profile_view", user.username)

        if request.user == user:
            if request.method == 'POST':
                try:
                    with transaction.atomic():
                        request_obj = Request.objects.get(Q(sender=exchanger), Q(receiver=user))
                        request_obj.status = Request.RequestStatus.ACCEPTED
                        request_obj.save()

                        sender_skill = request_obj.skill_to_exchange
                        receiver_skill = Skill.objects.get(pk=request.POST['skill_chosen'])

                        new_exchange = Exchanger(user=user, exchanger=exchanger, start_date=request_obj.start_date, end_date=request_obj.end_date)
                        new_exchange.save()
                        new_exchange.skills_exchanged.set([sender_skill, receiver_skill])
    
                        messages.success(request,"Request accepted.","alert-success")
                        
                except Exception as e:
                    messages.error(request, "Something went wrong, couldn't accept request.", "alert-danger")

        return redirect("accounts:profile_view", user.username)

    except Exception as e:
        messages.error(request, "Something went wrong, couldn't accept request", "alert-danger")
        return redirect("accounts:profile_view", user.username)

# Request details View
def request_details_view(request: HttpRequest, req_id: int):
    try:
        req = Request.objects.get(pk=req_id)
        if not ((req.sender == request.user) or (req.receiver == request.user)):
            messages.error(request, "You don't have permission to view this request.", "alert-warning")
            return redirect('main:home_view')
        
    except Exception as e:
        return render(request, '404.html')
    
    return render(request, 'exchangers/request_details.html', {'req': req})

# Request details View
def exchange_details_view(request: HttpRequest, exchange_id: int):
    try:
        exchange = Exchanger.objects.get(pk=exchange_id)
        if not ((exchange.user == request.user) or (exchange.exchanger == request.user)):
            messages.error(request, "You don't have permission to view this exchange.", "alert-warning")
            return redirect('main:home_view')
        
    except Exception as e:
        return render(request, '404.html')
    return render(request, 'exchangers/exchange_details.html', {'exchange': exchange})
