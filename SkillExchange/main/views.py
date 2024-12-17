from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from .models import Contact








# Create your views here.


# Home View

def home_view(request: HttpRequest):

    if request.method == "POST":
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            inquiries_type = request.POST["inquiries_type"]
            message = request.POST["message"]

            if not (name and email and inquiries_type and message):
                raise ValueError("All fields are required.")

            contact = Contact(
                name=name, email=email, inquiries_type=inquiries_type, message=message
            )
            contact.save()

            # Send confirmation email to the user
            content_html = render_to_string(
                "main/mail/confirmation.html", {"name": name}
            )
            user_email = EmailMessage(
                subject="We Got Your Message - Skill Exchange",
                body=content_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            user_email.content_subtype = "html"
            user_email.send()

            # Send notification email to admin
            content_html_admin = render_to_string(
                "main/mail/admin_notification.html",
                {
                    "name": name,
                    "email": email,
                    "inquiries_type": inquiries_type,
                    "message": message,
                },
            )

            admin_email = EmailMessage(
                subject="New Inquiry Received",
                body=content_html_admin,
                from_email=settings.EMAIL_HOST_USER,
                to=["khulood.u97@gmail.com"],
            )

            admin_email.content_subtype = "html"
            admin_email.send()

            messages.success(
                request, "Your message has been sent successfully!", "alert-success"
            )

            return redirect("main:home_view")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}", "alert-danger")
            return redirect("main:home_view")

    return render(request, "main/index.html")







