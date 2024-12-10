from django.urls import path
from . import views

app_name = "skills"

urlpatterns = [
    path('', views.skills_list, name='skills_list'),
    path('add/', views.add_skill, name='add_skill'),
    path('detail/<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
]