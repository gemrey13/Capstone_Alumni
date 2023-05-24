from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('job/', views.related_job, name="related_hob"),
    path('alumni/', views.alumni, name="alumni")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


