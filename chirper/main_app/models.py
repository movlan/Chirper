from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)

class Avatar(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"photo for UserId {self.user_id}"

class Chirp(models.Model):
    content = models.TextField(max_length=140, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('home')
