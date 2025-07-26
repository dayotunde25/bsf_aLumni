from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.index, name='index'),
    path('media/<int:media_id>/', views.media_detail, name='media_detail'),
    path('upload/', views.upload_media, name='upload_media'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_gallery, name='event_gallery'),
]
