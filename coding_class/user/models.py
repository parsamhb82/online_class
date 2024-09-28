from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self) -> str:
        return self.user.username
