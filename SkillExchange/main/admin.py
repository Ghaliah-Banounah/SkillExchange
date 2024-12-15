from django.contrib import admin
from .models import Contact, Plan, Subscription

# Register your models here.

admin.site.register (Contact)

admin.site.register (Plan)

admin.site.register (Subscription)