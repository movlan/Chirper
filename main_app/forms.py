from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Chirp, User

User = get_user_model()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.TextInput()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "bio")
    
class ChirpCreateForm(ModelForm):
    class Meta:
        model = Chirp 
        fields = ['content']
