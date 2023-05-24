from django.urls import path

from . import views


app_name = "AlumniManagement"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('job/', views.related_job, name="related_hob"),
    path('alumni/', views.alumni, name="alumni")
]


