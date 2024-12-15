from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from .models import Contact
from .models import Plan
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt







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






# Display Plans View

def plans_view(request):

    plans = Plan.objects.all()

    return render(request, "main/plans.html", {"plans":plans})





# Add Plan View

def add_plan_view(request):

    if request.method == "POST":
        plan_name = request.POST.get("plan_name")
        plan_feture_1 = request.POST.get("plan_feture_1")
        plan_feture_2 = request.POST.get ("plan_feture_2")
        plan_feture_3 = request.POST.get("plan_feture_3")
        plan_amount = request.POST.get("plan_amount")

        #validation
        if not all([plan_name, plan_feture_1, plan_feture_2, plan_feture_3, plan_amount]):
            messages.error(request, "All fields are required!")
            return render(request, "main/add_plan.html")
        
        try:
            
            plan_amount = int(plan_amount)

            new_plan = Plan(
                plan_name=plan_name,
                plan_feture_1=plan_feture_1,
                plan_feture_2=plan_feture_2,
                plan_feture_3=plan_feture_3,
                plan_amount=plan_amount,
            )
            new_plan.save()

            messages.success(request, "Plan added successfully!", "alert-success")
            return redirect("main:plans_view")
        
        
        except ValueError:
            messages.error(request, "Plan amount must be a valid number.", "alert-danger")
            return render(request, "main/add_plan.html")

    return render(request, "main/add_plan.html")





#Detail Plan View

def plan_detail_view(request, plan_id):

    plan = get_object_or_404(Plan, id=plan_id)

    return render(request, "main/plan_detail.html", {"plan": plan})





#Update Plane View

def update_plan_view(request, plan_id):

    from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Plan

def update_plan_view(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)  

    if request.method == "POST":
        plan.plan_name = request.POST.get("plan_name", plan.plan_name)
        plan.plan_feture_1 = request.POST.get("plan_feture_1", plan.plan_feture_1)
        plan.plan_feture_2 = request.POST.get("plan_feture_2", plan.plan_feture_2)
        plan.plan_feture_3 = request.POST.get("plan_feture_3", plan.plan_feture_3)
        plan.plan_amount = request.POST.get("plan_amount", plan.plan_amount)

        plan.save() 
        messages.success(request, "Plan updated successfully!", "alert-success")
        return redirect("main:plan_detail_view", plan_id=plan.id)  

    return render(request, "main/update_plan.html", {"plan": plan})







#Delete Plane View

def delete_plan_view(request, plan_id):

    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == 'POST':
        plan.delete()

        messages.success(request, 'Plan deleted successfully.', 'alert-danger')
        return redirect("main:plans_view")
      
    else:
        return render(request, 'main/plan_detail.html', {'plan': plan})










#Payment View

def payment_view(request, plan_id):
    
    plan = get_object_or_404(Plan, id=plan_id)  
    return render(request, "main/payment/payment.html", {"plan": plan})




#Success Payment View

def payment_success_view(request):

    return render(request, "main/payment/payment_success.html")





#Failed Payment View

def payment_failed_view(request):

    return render(request, "main/payment/payment_failed.html")




#CallBack View

@csrf_exempt
def callback_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            payment_status = data.get("status")  
            description = data.get("description")  
            plan_name = description.split()[0] if description else None  

            if payment_status == "paid" and plan_name:
                plan = Plan.objects.filter(plan_name__iexact=plan_name).first()
                if plan:
                    print(f"Payment Successful for Plan: {plan_name}")
                    return redirect("main:payment_success_view")

            print("Payment Failed or Plan not found")
            return redirect("main:payment_failed_view")

        except Exception as e:
            logging.exception("Error processing payment callback")
            return JsonResponse({"error": "Invalid callback data"}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)




