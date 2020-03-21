from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreateForm

def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreateForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreateForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)