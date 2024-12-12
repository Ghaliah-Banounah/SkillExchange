from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('send/<str:recipient_username>/', views.send_chat, name='send_chat')
]