from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('chirps/create/', views.ChirpCreate.as_view(), name='chirps_create'),
    path('chirps/<int:pk>/update/', views.ChirpUpdate.as_view(), name='chirps_update'),
    path('chirps/<int:pk>/delete/', views.ChirpDelete.as_view(), name='chirps_delete'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('user/<int:user_id>/add_avatar/', views.add_avatar, name='add_avatar'),
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    url(r'^password/$', views.change_password, name='change_password'),
]
