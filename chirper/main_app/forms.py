from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.TextInput()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "bio", )
    # def save(self, commit=True):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.bio = self.cleaned_data["bio"]
    #     if commit:
    #         user.save()
    #     return user