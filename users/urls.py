from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('directory/', views.directory, name='directory'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
