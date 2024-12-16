from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    pfp = models.ImageField(upload_to="images/exchangers/", default="images/exchangers/defaultPfp.jpg")
    linkedin_url = models.URLField()
    phone = models.CharField(max_length=10)
    skills = models.ManyToManyField(Skill, related_name='skills')
    skills_needed = models.ManyToManyField(Skill, related_name='skills_needed')
    is_online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Profile {self.user.username}'
    
class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "Bad"
        STAR2 = 2, "Acceptable"
        STAR3 = 3, "Good"
        STAR4 = 4, "Great"
        STAR5 = 5, "Awesome"

    exchanger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_owner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} on {self.exchanger.first_name}"
