from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_hub, name='resource_hub'),
    path('<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('upload/', views.upload_resource, name='upload_resource'),
    path('<int:resource_id>/download/', views.download_resource, name='download_resource'),
    path('<int:resource_id>/rate/', views.rate_resource, name='rate_resource'),
    path('<int:resource_id>/bookmark/', views.bookmark_resource, name='bookmark_resource'),
    path('my-bookmarks/', views.my_bookmarks, name='my_bookmarks'),
]
