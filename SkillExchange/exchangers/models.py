from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from skills.models import Skill

class Exchanger(models.Model):
    class ExchangeStatus(models.TextChoices):
        ONGOING = 'Ongoing', 'Ongoing'
        ENDED = 'Ended', 'Ended'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanger")
    exchanger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanging_with")
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    skills_exchanged = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ExchangeStatus.choices, default=ExchangeStatus.ONGOING)
    
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
    skill_to_exchange = models.OneToOneField(Skill, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} - {self.status}"
