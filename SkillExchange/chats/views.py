from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Chat
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Profile

@login_required
def chat_list(request):
    users_in_conversation = User.objects.exclude(id=request.user.id)

    users_in_conversation = [
        user for user in users_in_conversation
        if Chat.objects.filter(Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user)).exists()
    ]

    for user in users_in_conversation:
        user.unread_messages_count = Chat.objects.filter(sender=user, receiver=request.user, read_at__isnull=True).count()

        last_message = Chat.objects.filter(
            Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user)
        ).order_by('-sent_at').first()

        if last_message:
            user.last_message = last_message.content
            user.last_message_time = last_message.sent_at.strftime('%Y-%m-%d %H:%M')
        else:
            user.last_message = "No messages yet"
            user.last_message_time = "No messages yet"

        time_diff = timezone.now() - user.last_login if user.last_login else timezone.timedelta(days=1)
        user.is_online = False

    users_in_conversation = sorted(users_in_conversation, key=lambda user: user.last_message_time, reverse=True)

    return render(request, 'chats/chats_list.html', {'users_in_conversation': users_in_conversation})


@login_required
def chat_view(request, user_id):
    receiver = User.objects.get(id=user_id)
    profile, created = Profile.objects.get_or_create(user=receiver)
    try:
        receiver_profile = Profile.objects.get(user=receiver)
        receiver.is_online = receiver_profile.is_online  
    except Profile.DoesNotExist:
        receiver.is_online = False
    
    conversation_id = str(min(request.user.id, receiver.id)) + "-" + str(max(request.user.id, receiver.id))

    messages = Chat.objects.filter(conversation_id=conversation_id).order_by('sent_at')

    users_in_conversation = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).exclude(id=request.user.id).distinct() 

    for user in users_in_conversation:
        user.unread_messages_count = Chat.objects.filter(sender=user, receiver=request.user, read_at__isnull=True).count()
        profile = Profile.objects.get(user=user)
        user.is_online = profile.is_online

        last_message = Chat.objects.filter(
            Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user)
        ).order_by('-sent_at').first()

        if last_message:
            user.last_message = last_message.content
            user.last_message_time = last_message.sent_at.strftime('%Y-%m-%d %H:%M')
        else:
            user.last_message = "No messages yet"
            user.last_message_time = "No messages yet"
        
        #time_diff = timezone.now() - user.last_login if user.last_login else timezone.timedelta(days=1)
        #is_chat_page= resolve(request.path_info).url_name
        #if is_chat_page == 'chat_view':
            #user_id=resolve(request.path_info).kwargs.get('user_id',None)
            #user.is_online = True
        #elif is_chat_page =='chat_list':
            #user.is_online = False

    users_in_conversation = sorted(users_in_conversation, key=lambda user: user.last_message_time, reverse=True)

    if request.method == 'POST':
        content = request.POST.get('message')
        file = request.FILES.get('file')

        if content or file:
            chat_message = Chat.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                conversation_id=conversation_id,
                file=file
            )

            Chat.objects.filter(sender=receiver, receiver=request.user, read_at__isnull=True).update(read_at=timezone.now())

            return redirect('chats:chat_view', user_id=user_id)

    Chat.objects.filter(sender=receiver, receiver=request.user, read_at__isnull=True).update(read_at=timezone.now())

    return render(request, 'chats/send_message.html', {
        'messages': messages,
        'receiver': receiver,
        'users_in_conversation': users_in_conversation,
    })


@login_required
def delete_chat(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    chats = Chat.objects.filter(
        (Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user))
    )
    
    if not chats.exists():
        return redirect('chats:chat_list') 
    
    if request.user == chats.first().sender:
        chats.delete()

    else:
        chats.filter(sender=user).delete() 
    
    return redirect('chats:chat_list')


@receiver(user_logged_in)
def update_last_seen_on_login(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.is_online = True  
    profile.last_seen = timezone.now()  
    profile.save()


@receiver(user_logged_out)
def update_last_seen_on_logout(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.is_online = False 
    profile.last_seen = timezone.now()  
    profile.save()
