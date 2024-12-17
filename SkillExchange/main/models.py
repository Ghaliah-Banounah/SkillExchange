from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Contact(models.Model):
    class InquiriesType(models.TextChoices):
        GENERAL_QUESTIONS = "General Questions", "General Questions"
        TECHNICAL_SUPPORT = "Technical Support", "Technical Support"
        FEEDBACK_OR_SUGGESTIONS = "Feedback or Suggestions", "Feedback or Suggestions"
        ACCOUNT_ISSUES = "Account Issues", "Account Issues"
        SUBSCRIPTION_AND_PAYMENTS = "Subscription and Payments", "Subscription and Payments"
        SKILL_EXCHANGE_REQUESTS = "Skill Exchange Requests", "Skill Exchange Requests"
        OTHER = "Other", "Other"
        
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    inquiries_type = models.CharField(
        max_length=100,
        choices=InquiriesType.choices,
        blank=True,
        null=True
    )


    def __str__(self):
        return f"Message from {self.name}"
    

    class Meta:
        ordering = ['-created_at']
