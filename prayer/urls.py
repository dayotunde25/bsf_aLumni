from django.urls import path
from . import views

app_name = 'prayer'

urlpatterns = [
    path('', views.prayer_wall, name='prayer_wall'),
    path('request/<int:prayer_id>/', views.prayer_detail, name='prayer_detail'),
    path('add-request/', views.add_prayer_request, name='add_prayer_request'),
    path('pray/<int:prayer_id>/', views.pray_for_request, name='pray_for_request'),
    path('testimonies/', views.testimonies, name='testimonies'),
    path('add-testimony/', views.add_testimony, name='add_testimony'),
    path('like-testimony/<int:testimony_id>/', views.like_testimony, name='like_testimony'),
]
