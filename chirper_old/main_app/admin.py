from django.contrib import admin
from .models import User, Chirp, Avatar, Follower

admin.site.register(User)
admin.site.register(Chirp)
admin.site.register(Avatar)
admin.site.register(Follower)