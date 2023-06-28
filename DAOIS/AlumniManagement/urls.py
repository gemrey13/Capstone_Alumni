from django.urls import path
from . import views

app_name = "AlumniManagement"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('alumni/', views.alumni, name="alumni"),
    path('alumni/<str:alumni_id>/', views.alumni_profile, name='alumni_profile'),

    path('sample2/', views.sample2, name="sample2"),

    path('get_provinces/', views.get_provinces, name='get-provinces'),
    path('get_cities/', views.get_cities, name='get-cities'),
    path('get_barangays/', views.get_barangays, name='get-barangays'),

    path('delete_currrent_job/<str:job_id>/', views.del_current_job, name='delete_currrent_job'),
    path('delete_prev_job/<str:job_id>/', views.del_prev_job, name='delete_prev_job'),
    path('delete_alumni/<str:alumni_id>/', views.del_alumni, name='delete_alumni'),
]