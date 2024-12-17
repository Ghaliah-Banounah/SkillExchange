from django.urls import path
from . import views

app_name = "plans"

urlpatterns = [
    path('', views.plans_view, name='plans_view'),
    path('add/', views.add_plan_view, name='add_plan_view'),
    path('detail/<plan_id>', views.plan_detail_view, name='plan_detail_view'),
    path('update/<plan_id>', views.update_plan_view, name='update_plan_view'),
    path('delete/<plan_id>', views.delete_plan_view, name='delete_plan_view'),
    path('payment/<plan_id>/', views.payment_view, name='payment_view'),
    path('payment/<plan_id>/result/', views.payment_result_view, name='payment_success_view'),
]