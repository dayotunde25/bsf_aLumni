from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_board, name='job_board'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('post/', views.post_job, name='post_job'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('<int:job_id>/save/', views.save_job, name='save_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
]
