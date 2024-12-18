from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from .models import Contact
from django.db.models import Avg
from exchangers.models import Exchanger
from django.contrib.auth.models import User
from .models import Testimony
from django.contrib.auth.decorators import login_required










# Create your views here.


# Home View

def home_view(request: HttpRequest):

    exchangers = Exchanger.objects.annotate(average_rating=Avg("user__reviews__rating")).filter(average_rating__gte=4).order_by("-average_rating")[:4]
    testimonies = Testimony.objects.all().order_by("-created_at")[:4]

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

    return render(request, "main/index.html", {"exchangers": exchangers, "testimonies": testimonies})




def testimony_view(request: HttpRequest,user_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You Need to login to Write Testimony", "alert-warning")
        return redirect("main:home_view")

    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        testimony_comment = request.POST.get("testimony_comment", "").strip()

        if testimony_comment:
            Testimony.objects.create(user=user, testimony_comment=testimony_comment)
            messages.success(request, "Your testimony has been added successfully!", "alert-success")
            return redirect("main:home_view")

    return render(request, "main/testimony.html")




@login_required
def delete_testimony(request, testimony_id):
    
    if not request.user.is_staff and not request.user.has_perm("main.delete_testimony"):
        messages.warning(request, "You don't have permission to delete this testimony.", "alert-warning")
        return redirect("main:home_view")
    
    testimony = get_object_or_404(Testimony, id=testimony_id)
    
    
    try:
        testimony.delete()
        messages.success(request, "Testimony deleted successfully!", "alert-success")

    except Exception as e:
        messages.error(request, "Something went wrong. Could not delete the testimony.", "alert-danger")
    
    return redirect("main:home_view") 
