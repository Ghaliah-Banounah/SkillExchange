from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('plans/', views.plans_view, name='plans_view'),
    path('add/', views.add_plan_view, name='add_plan_view'),
    path('payment/<plan_type>/', views.payment_view, name='payment_view'),

]