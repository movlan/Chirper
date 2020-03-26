from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreateForm, ChirpCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Chirp, Avatar, User, Follower
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'chirp-chirp'

@login_required
def add_avatar(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Avatar(url=url, user_id=user_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile', user_id=user_id)

class ChirpCreate(LoginRequiredMixin, CreateView):
    model = Chirp
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class ChirpUpdate(LoginRequiredMixin, UpdateView):
    model = Chirp
    fields = ['content']

class ChirpDelete(LoginRequiredMixin, DeleteView):
    model = Chirp
    success_url = '/'

def home(request):
    chirps = Chirp.objects.all()
    return render(request, 'home.html', {'chirps': chirps, 'chirp_form': ChirpCreateForm() })

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

@login_required
def profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    is_following = False
    if request.user.is_authenticated:
        is_following = profile_user.followers.filter(follower=request.user).exists()
    followed_count = profile_user.followers.all().count()
    following_count = profile_user.following.all().count()
    return render(request, 'main_app/user_profile.html', 
        {
            'user_id': user_id,
            'profile_user': profile_user,
            'followed_count': followed_count,
            'following_count': following_count,
            'is_following': is_following,
        })

@login_required
def follow(request, user_id):
    user_1 = request.user
    user_2 = User.objects.get(id=user_id)
    Follower(following=user_2, follower=user_1).save()
    return redirect('profile', user_id=user_id)

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email", "bio"]

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main_app/change_password.html', {
        'form': form
    })

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'

@login_required
def my_nest(request):
    following = request.user.following.all()
    print(list(following))
    return render(request, 'main_app/my_nest.html', { 'following': following })

