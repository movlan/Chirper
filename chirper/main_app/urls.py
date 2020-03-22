from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('chirps/create/', views.ChirpCreate.as_view(), name='chirps_create'),
    path('chirps/<int:pk>/update/', views.ChirpUpdate.as_view(), name='chirps_update'),
    path('chirps/<int:pk>/delete/', views.ChirpDelete.as_view(), name='chirps_delete'),
    path('user/<int:user_id>/add_avatar/', views.add_avatar, name='add_avatar'),
    path('user/<int:user_id>/', views.profile, name='profile'),
]
