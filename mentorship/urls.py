from django.urls import path
from . import views

app_name = 'mentorship'

urlpatterns = [
    path('', views.mentors, name='mentors'),
    path('mentor/<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
    path('become-mentor/', views.become_mentor, name='become_mentor'),
    path('request/<int:mentor_id>/', views.request_mentorship, name='request_mentorship'),
    path('mentor-dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentee-dashboard/', views.mentee_dashboard, name='mentee_dashboard'),
    path('respond/<int:request_id>/', views.respond_to_request, name='respond_to_request'),
]
