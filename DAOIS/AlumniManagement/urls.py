from django.urls import path

from . import views


app_name = "AlumniManagement"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('alumni/', views.alumni, name="alumni"),
    path('sample/', views.sample, name="sample"),
]


