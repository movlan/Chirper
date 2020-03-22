from django.contrib import admin
from .models import User, Chirp, Avatar

admin.site.register(User)
admin.site.register(Chirp)
admin.site.register(Avatar)