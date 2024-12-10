from django.shortcuts import render , redirect ,  get_object_or_404
from .forms import SkillForm
from .models import Skill
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def skills_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        skills_list = Skill.objects.filter(name__icontains=search_query)
        if not skills_list:
            messages.info(request, 'No results found')
    else:
        skills_list = Skill.objects.all()

    paginator = Paginator(skills_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'skills/skills_list.html', {'skills': page_obj})

def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('skills:skills_list')
    else:
        form = SkillForm() 

    return render(request, 'skills/add_skill.html', {'form': form})

def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    return render(request, 'skills/skill_detail.html', {'skill': skill})

def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully')
            return redirect('skills:skills_list')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'skills/edit_skill.html', {'form': form, 'skill': skill})

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully.')
        return redirect('skills:skills_list')  
    else:
        return render(request, 'skills/skill_detail.html', {'skill': skill})