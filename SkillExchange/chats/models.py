from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    conversation_id = models.CharField(max_length=255 , null=False, default=uuid.uuid4) 
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)  

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.sent_at}"

    class Meta:
        ordering = ['sent_at']
    #@property
    #def is_sender_online(self):
        #return self.sender.is_online

    #@property
    #def is_receiver_online(self):
        #return self.receiver.is_online