from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'pfp', 'skills', 'skills_needed', 'linkedin_url', 'phone']