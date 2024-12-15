from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Chat
import uuid 
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

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
        user.is_online = time_diff < timezone.timedelta(minutes=1)

    users_in_conversation = sorted(users_in_conversation, key=lambda user: user.last_message_time, reverse=True)

    return render(request, 'chats/chats_list.html', {'users_in_conversation': users_in_conversation})


@login_required
def chat_view(request, user_id):
    receiver = User.objects.get(id=user_id)

    conversation_id = str(min(request.user.id, receiver.id)) + "-" + str(max(request.user.id, receiver.id))

    messages = Chat.objects.filter(conversation_id=conversation_id).order_by('sent_at')

    users_in_conversation = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).exclude(id=request.user.id).distinct() 

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
        user.is_online = time_diff < timezone.timedelta(minutes=1)

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