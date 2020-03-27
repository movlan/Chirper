from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.id})

class Avatar(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"photo for UserId {self.user_id}"

class Chirp(models.Model):
    content = models.TextField(max_length=140, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['-id']

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return u'%s follows %s' % (self.follower, self.following)
