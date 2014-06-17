from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
	return render(request, 'gk/Home.html')

def goal(request):
	return render(request, 'gk/Goal.html')

def action(request):
	return render(request, 'gk/Actions.html')

def contacts(request):
	return render(request, 'gk/Contacts.html')

def profile(request):
	return render(request, 'gk/Profile.html')