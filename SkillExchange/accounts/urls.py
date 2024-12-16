from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name="register_view"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('profile/update/', views.update_profile_view, name="update_profile_view"),
    path('profile/<username>/', views.profile_view, name="profile_view"),

    path("reviews/add/<exchanger_id>/", views.add_review_view, name="add_review_view"),
    path("reviews/delete/<review_id>/", views.delete_review_view, name="delete_review_view"),
]