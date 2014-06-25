from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from gk.models import *

# Create your views here.


def home(request):
	latest_goals = Goal.objects.order_by('name')[:5]
	actions = Action.objects.all()
	context = {'latest_goals' : latest_goals,
				'actions' : actions}
	return render(request, 'gk/Home.html', context)

def goal(request, goal_name):
	goal = get_object_or_404( Goal, name=goal_name)
	actions = Action.objects.filter(goal = goal)
	completed_actions = [a for a in actions if a.completed]
	pending_actions = [a for a in actions if not a.completed]
	recent_status_updates = StatusUpdate.objects.filter(goal = goal).order_by('-pub_time')[:3]
	caregivers = Caregiver.objects.filter(goal = goal)
	context = {'goal' : goal,
			   'actions' : actions,
			   'pending_actions' : pending_actions,
			   'completed_actions' : completed_actions,
			   'recent_status_updates' : recent_status_updates,
			   'caregivers' : caregivers,
			   }
	return render(request, 'gk/Goal.html', context)

def action(request):
	actions = Action.objects.order_by('-deadline')
	completed_actions = [a for a in actions if a.completed]
	pending_actions = [a for a in actions if not a.completed]
	context = {'actions' : actions,
			   'pending_actions' : pending_actions,
			   'completed_actions' : completed_actions,
			   }
	return render(request, 'gk/Actions.html', context)

def contacts(request):
	caregivers = Caregiver.objects.all()
	context = {'caregivers' : caregivers,
			   }
	return render(request, 'gk/Contacts.html', context)

def profile(request):
	patient = Patient.objects.all()[:1]
	updates = StatusUpdate.objects.order_by('-pub_time')[:5]
	context = {'patient' : patient,
			   'updates' : updates,
			   }
	return render(request, 'gk/Profile.html', context)






