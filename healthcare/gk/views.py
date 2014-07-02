from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from gk.models import *
from django import forms
import datetime

# Create your views here.


def home(request):
	if (request.method == 'POST'):
		form = AddGoalForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['goal_Name']
			type = form.cleaned_data['Type']
			notes = form.cleaned_data['Description']
			active = True
			patient = get_object_or_404(Patient, name="Billy Smith")
			caregiverName = form.cleaned_data['caregiver']
			caregiver = get_object_or_404(Caregiver, name = caregiverName)
			newGoal = Goal.objects.create(name = name, 
										  notes = notes, 
										  active = active, 
										  caregiver = caregiver, 
										  patient = patient,
										  )
			return HttpResponseRedirect('')
	else:
		form = AddGoalForm()

	latest_goals = Goal.objects.order_by('name')[:5]
	actions = Action.objects.all()
	context = {'latest_goals' : latest_goals,
				'actions' : actions,
				'AddGoalForm' : AddGoalForm,
				}
	return render(request, 'gk/Home.html', context)



def goal(request, goal_name):
	if (request.method == 'POST'):
		if (request.POST['key'] == 'stat'):
			form = AddStatusForm(request.POST)
			if form.is_valid():
				notes = form.cleaned_data['status']
				data_value = form.cleaned_data['data_Value']
				pub_time = datetime.datetime.now()
				reporting_caregiver = get_object_or_404(Caregiver, name = "Dr. Logan Martin")
				status = "N/A"
				goal = get_object_or_404( Goal, name=goal_name)
				NEW_STATUS = StatusUpdate.objects.create(goal=goal,
														 notes = notes,
														 data_value=data_value,
														 pub_time=pub_time,
														 reporting_caregiver=reporting_caregiver,
														 status=status,
														 )
				return HttpResponseRedirect('')
		
		elif (request.POST['key'] == 'act'):
			form = AddActionForm_GoalPage(request.POST)
			if form.is_valid():
				goal = get_object_or_404( Goal, name=goal_name)
				name = form.cleaned_data['action']
				deadline = form.cleaned_data['due_Date']
				notes = "N/A"
				caregiver = get_object_or_404(Caregiver, name = "Dr. Logan Martin")
				completed = False
				NEW_ACTION = Action.objects.create(goal = goal, 
												   name = name, 
												   deadline=deadline, 
												   caregiver=caregiver, 
												   notes=notes, 
												   completed=completed,
												   )
				return HttpResponseRedirect('')

	else:
		form1 = AddActionForm_GoalPage()
		form2 = AddStatusForm()

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
			   'AddActionForm_GoalPage' : AddActionForm_GoalPage,
			   'AddStatusForm' : AddStatusForm,
			   }
	return render(request, 'gk/Goal.html', context)


def action(request):
	
	if (request.method == 'POST'):
		if ('actionForm' in request.POST):
			form = AddActionForm_ActionPage(request.POST)
			if form.is_valid():
				goal_name = form.cleaned_data['goal']
				goal = get_object_or_404(Goal, name=goal_name)
				name = form.cleaned_data['action']
				deadline = form.cleaned_data['due_Date']
				notes = "N/A"
				caregiver = get_object_or_404(Caregiver, name = "Dr. Logan Martin")
				completed = False
				NEW_ACTION = Action.objects.create(goal = goal, 
												   name = name, 
												   deadline=deadline, 
												   caregiver=caregiver, 
												   notes=notes, 
												   completed=completed,
												   )
				
				return HttpResponseRedirect('')

		elif ('Complete' in request.POST):
			action = get_object_or_404(Action, id=request.POST.get('actionName', False))
			action.completed = True
			action.save()
			return HttpResponseRedirect('')
		elif ('remove' in request.POST):
			action = get_object_or_404(Action, id=request.POST.get('actionName', False))
			action.delete()
			return HttpResponseRedirect('')

	else:
		form = AddActionForm_ActionPage()

	actions = Action.objects.order_by('-deadline')
	completed_actions = [a for a in actions if a.completed]
	pending_actions = [a for a in actions if not a.completed]
	context = {'actions' : actions,
			   'pending_actions' : pending_actions,
			   'completed_actions' : completed_actions,
			   'AddActionForm_ActionPage' : AddActionForm_ActionPage,
			   }
	return render(request, 'gk/Actions.html', context)



def contacts(request):
	if (request.method == 'POST'):
		form = AddContactForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['contact_Name']
			role = form.cleaned_data['Role']
			email = form.cleaned_data['Email']
			phone = form.cleaned_data['Phone']
			NEW_CONTACT = Caregiver.objects.create(name = name, 
												   role = role, 
												   email = email, 
												   phone = phone,
												   )
			return HttpResponseRedirect('')
	else:
		form = AddContactForm()
	caregivers = Caregiver.objects.all()
	context = {'caregivers' : caregivers,
			   'AddContactForm' : AddContactForm
			   }
	return render(request, 'gk/Contacts.html', context)



def profile(request):
	patient = Patient.objects.all()[:1]
	updates = StatusUpdate.objects.order_by('-pub_time')[:5]
	context = {'patient' : patient,
			   'updates' : updates,
			   }
	return render(request, 'gk/Profile.html', context)



############### Form Classes ###############



class AddGoalForm(forms.Form):
	type_choices = [('0', u'Qualitative'), 
					('1', u'Quantitative'),
					]
	caregiver_choices = []
	for c in Caregiver.objects.all():
		caregiver_choices.append((c.name, c))
	goal_Name = forms.CharField(max_length = 30)
	Type = forms.ChoiceField(type_choices)
	Description = forms.CharField()
	caregiver = forms.ChoiceField(caregiver_choices)

class AddContactForm(forms.Form):
	contact_Name = forms.CharField()
	Role = forms.CharField()
	Email = forms.EmailField()
	Phone = forms.CharField()

class AddActionForm_ActionPage(forms.Form):
	goal_choices = []
	for g in Goal.objects.all():
		goal_choices.append((g.name, g))

	goal = forms.ChoiceField(goal_choices)
	action = forms.CharField()
	due_Date = forms.DateField()

class AddActionForm_GoalPage(forms.Form):
	action = forms.CharField()
	due_Date = forms.DateField()

class AddStatusForm(forms.Form):
	status = forms.CharField()
	data_Value = forms.IntegerField()

class complete_button(forms.Form):
	pass










