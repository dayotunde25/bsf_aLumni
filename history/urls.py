from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.fellowship_history, name='fellowship_history'),
    path('timeline/', views.timeline, name='timeline'),
    path('executives/', views.executives, name='executives'),
    path('executives/<int:executive_id>/', views.executive_detail, name='executive_detail'),
    path('milestones/', views.milestones, name='milestones'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('contribute/', views.contribute_history, name='contribute_history'),
]
