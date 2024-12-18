from django.shortcuts import render , redirect ,  get_object_or_404
from .forms import SkillForm
from .models import Skill
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from accounts.models import Profile

# All skills View
def skills_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        skills_list = Skill.objects.filter(name__icontains=search_query).order_by('-added_at')

    else:
        skills_list = Skill.objects.all().order_by('-added_at')
    
    skills_list = skills_list.annotate(exchangers_count=Count("skills"))

    paginator = Paginator(skills_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'skills/skills_list.html', {'skills': page_obj})

# Add skill View
def add_skill(request):
    if not (request.user.is_staff and request.user.has_perm('skills.add_skill')):
        messages.warning(request, "You don't have permission to add skills.", "alert-warning")
        return redirect('main:home_view')
    
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was added successfully.", "alert-success")
            return redirect('skills:skills_list')
        else:
            messages.error(request, f"{form.errors.as_data()}, skill wasn't added.", "alert-danger")

    return render(request, 'skills/add_skill.html', {'form': form})

# Skill detials View
def skill_detail(request, skill_id):
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Exception as e:
        return render(request, '404.html')
    
    exchangers = User.objects.filter(profile__skills__id=skill.id)[0:3]
    return render(request, 'skills/skill_detail.html', {'skill': skill, 'skill_exchangers': exchangers})

# Update skill View
def edit_skill(request, skill_id):
    if not (request.user.is_staff and request.user.has_perm('skills.change_skill')):
        messages.warning(request, "You don't have permission to update skills.", "alert-warning")
        return redirect('main:home_view')
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Exception as e:
        return render(request, '404.html')

    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully' , 'alert-primary')
            return redirect('skills:skill_detail', skill.id)
        else:
            messages.error(request, f"{form.errors.as_data()}, skill wasn't updated.", "alert-danger")

    return render(request, 'skills/edit_skill.html', {'form': form, 'skill': skill})

# Delete skill View
def delete_skill(request, skill_id):
    if not (request.user.is_staff and request.user.has_perm('skills.delete_skill')):
        messages.warning(request, "You don't have permission to delete skills.", "alert-warning")
        return redirect('main:home_view')
    
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Exception as e:
        return render(request, '404.html')
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully.', 'alert-success')
        return redirect('skills:skills_list')  
    else:
        return render(request, 'skills/skill_detail.html', {'skill': skill})
    