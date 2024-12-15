from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
    path('delete_chat/<int:user_id>/', views.delete_chat, name='delete_chat'),
]
