from django.contrib import admin
from .models import User, Chirp

admin.site.register(User)
admin.site.register(Chirp)