import requests
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from .models import Contact
from .models import Plan
from .models import Subscription
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta



# Create your views here.
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





def plans_view(request):

    plans = Plan.objects.all()

    return render(request, "main/plans.html", {"plans":plans})



def add_plan_view(request):

    if request.method == "POST":
        plan_name = request.POST.get["plan_name"]
        plan_feture_1 = request.POST.get["plan_feture_1"]
        plan_feture_2 = request.POST.get ["plan_feture_2"]
        plan_feture_3 = request.POST.get["plan_feture_3"]
        plan_amount = request.POST.get["plan_amount"]
        
        new_plan = Plan(plan_name=plan_name, plan_feture_1=plan_feture_1, plan_feture_2=plan_feture_2, plan_feture_3=plan_feture_3, plan_amount=plan_amount)
        new_plan.save()


        messages.success(request, "Plan added successfully!")
        return redirect("main:plans_view")

    return render(request, "main/add_plan.html")




def payment_view(request, plan_type):

    return render(request, "main/payment.html", {"plan_type": plan_type})




@csrf_exempt
def subscription_callback(request):
    if request.method == "POST":
        try:
            # Parse the JSON data sent by Moyasar
            data = json.loads(request.body.decode("utf-8"))
            payment_status = data.get("status")
            payment_id = data.get("id")
            plan_description = data.get("description")
            user_email = data.get("source", {}).get("email")

            # Validate payment status
            if payment_status == "paid" and "Premium Plan" in plan_description:
                user, created = User.objects.get_or_create(email=user_email)
                if created:
                    user.username = user_email.split("@")[0]
                    user.save()

                # Update or create subscription
                subscription, created = Subscription.objects.get_or_create(user=user)
                subscription.is_active = True
                subscription.plan = "premium"
                subscription.start_date = now()
                subscription.end_date = now() + timedelta(days=30)
                subscription.save()

                logger.info(f"Subscription updated for user: {user_email}")
                return JsonResponse(
                    {"message": "Payment processed and subscription activated."},
                    status=200,
                )

            else:
                logger.warning("Payment failed or invalid data received.")
                return JsonResponse(
                    {"message": "Payment failed or invalid data."}, status=400
                )

        except Exception as e:
            logger.exception("Error processing callback data.")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)
