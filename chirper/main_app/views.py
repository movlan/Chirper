from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Chirp

class ChirpCreate(CreateView):
    model = Chirp
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class ChirpUpdate(UpdateView):
    model = Chirp
    fields = ['content']

class ChirpDelete(DeleteView):
    model = Chirp
    success_url = '/'

def home(request):
    chirps = Chirp.objects.all()
    return render(request, 'home.html', {'chirps': chirps})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreateForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)