from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('testimony/<user_id>/', views.testimony_view, name="testimony_view"),
    path("testimony/delete/<int:testimony_id>/", views.delete_testimony, name="delete_testimony"),

]