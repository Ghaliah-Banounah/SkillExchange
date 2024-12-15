from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('plans/', views.plans_view, name='plans_view'),
    path('add/', views.add_plan_view, name='add_plan_view'),
    path('detail/<plan_id>', views.plan_detail_view, name='plan_detail_view'),
    path('update/<plan_id>', views.update_plan_view, name='update_plan_view'),
    path('delete/<plan_id>', views.delete_plan_view, name='delete_plan_view'),
    path('payment/<plan_id>/', views.payment_view, name='payment_view'),
    path('payment/success/', views.payment_success_view, name='payment_success_view'),
    path('payment/failed/', views.payment_failed_view, name='payment_failed_view'),
    path('payment/callback/', views.callback_view, name='callback_view'),

]