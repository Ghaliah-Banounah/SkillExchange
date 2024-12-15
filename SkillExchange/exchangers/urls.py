from django.urls import path
from . import views

app_name = "exchangers"

urlpatterns = [
    path("send/request/<sender_id>/<receiver_id>/",views.send_request_view,name="send_request_view"),
    path("reject/request/<sender_id>/<receiver_id>/",views.reject_request_view,name="reject_request_view"),
    path("new/exchange/<sender_id>/<receiver_id>/",views.new_exchange_view,name="new_exchange_view"),

    path('all/', views.display_exchangers_view, name="display_exchangers_view"),
]