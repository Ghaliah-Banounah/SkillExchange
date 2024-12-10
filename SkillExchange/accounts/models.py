from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    pfp = models.ImageField(upload_to="images/exchangers/", default="images/exchangers/defaultPfp.jpg")
    linkedin_url = models.URLField()
    phone = models.CharField(max_length=10)
    #skills
    #skills_needed

    def __str__(self) -> str:
        return f'Profile {self.user.username}'
