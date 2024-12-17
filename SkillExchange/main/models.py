from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta




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




class PLANTYPE(models.TextChoices):
        FREE = "Free", "Free"
        PREMIUM = "Premium", "Premium"

class Plan(models.Model):
    plan_name = models.CharField(max_length=50, choices=PLANTYPE, blank=True, null=True)
    plan_feture_1 = models.TextField(blank=True, null=True)
    plan_feture_2 = models.TextField(blank=True, null=True)
    plan_feture_3 = models.TextField(blank=True, null=True)
    plan_amount = models.PositiveIntegerField(default=0)



class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)



    #Auto-generate end_date
    def save(self, *args, **kwargs):
        if self.plan and self.plan.plan_name == "Premium" and not self.end_date:
            self.end_date = now() + timedelta(days=30)  
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.is_active and self.end_date and now() <= self.end_date

    def __str__(self):
        return f"{self.user.username} - {self.plan.plan_name if self.plan else 'No Plan'}"
