from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):
    bio = forms.Textarea()
    class Meta:
        model = User
        fields = ("username", "bio", "email", "password1", "password2", )
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.bio = self.cleaned_data["bio"]
        if commit:
            user.save()
        return user