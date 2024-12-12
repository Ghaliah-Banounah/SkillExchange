from django.shortcuts import render , redirect
from .models import Chat
from .forms import ChatForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
@login_required
def chat_list(request):
    sent_chats = Chat.objects.filter(sender=request.user).order_by('sent_at')
    received_chats = Chat.objects.filter(receiver=request.user).order_by('sent_at')

    return render(request, 'chat/chat_list.html', {
        'sent_chats': sent_chats,
        'received_chats': received_chats,
    })

@login_required
def send_chat(request, recipient_username):
    recipient = User.objects.get(username=recipient_username)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            chat = Chat(sender=request.user, receiver=recipient, content=content)
            chat.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('chat:chat_list') 
        else:
            messages.error(request, 'Message content cannot be empty.')

    return render(request, 'chat/send_messages.html', {'recipient_username': recipient_username})