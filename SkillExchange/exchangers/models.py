from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Exchanger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanger")
    exchanger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanging_with")
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.exchanger.username}"
    class Meta:
        unique_together = ('user', 'exchanger') #Prevent duplicate exchanges


class Request(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_request")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_request")
    status = models.CharField(max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    scheduled_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} - {self.status}"
