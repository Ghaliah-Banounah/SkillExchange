from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    sender = models.ForeignKey(User , related_name='sent_messages',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User , related_name='received_messages',on_delete=models.CASCADE)
    content=models.TextField()
    sent_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    login_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat from {self.sender.username} to {self.receiver.username} at {self.sent_at}'

    