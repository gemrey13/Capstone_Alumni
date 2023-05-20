from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard),
    path('job/', views.related_job),
]