from django.urls import path
from . import views


app_name = "AlumniManagement"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('alumni/', views.alumni, name="alumni"),
    path('alumni/<str:alumni_id>/', views.alumni_profile, name='alumni_profile'),
    path('alumni/search/', views.alumni_search, name='alumni_search'),

    path('sample/', views.sample, name="sample"),
    path('your/', views.your_view, name="your"),


    path('get_provinces/', views.get_provinces, name='get-provinces'),
    path('get_cities/', views.get_cities, name='get-cities'),
    path('get_barangays/', views.get_barangays, name='get-barangays'),
]


