from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Chirp, Avatar, User, Follower
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'chirp-chirp'

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


def follow(request, user_id):
    user_1 = request.user
    user_2 = User.objects.get(id=user_id)
    Follower(following=user_2, follower=user_1).save()