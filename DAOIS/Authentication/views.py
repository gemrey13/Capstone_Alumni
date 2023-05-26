from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('AlumniManagement:dashboard')
		else:
			messages.error(request, 'Invalid Username or password.')
			return redirect('Authentication:login')

	if messages.get_messages(request):
		messages.get_messages(request).used = True
	return render(request, 'Authentication/login.html')

def logout_view(request):
	logout(request)
	return redirect('Authentication:login')

def register_view(request):
	pass