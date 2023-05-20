from django.shortcuts import render
from .models import Alumni_Demographic_Profile
# Create your views here.
def dashboard(request):

	alumni = Alumni_Demographic_Profile.objects.all().values()
	return render(request, 'AlumniManagement/Dashboard.html', {
		'alumni': alumni
		})