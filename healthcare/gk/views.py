from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from gk.models import *
from django import forms
from chartit import DataPool, Chart
from django.utils import simplejson
import datetime
import time
from django.core import serializers




# Create your views here.


def home(request):
	if (request.method == 'POST'):
		form = AddGoalForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['goal_Name']
			data_type = form.cleaned_data['Type']
			notes = form.cleaned_data['Description']
			active = True
			patientName = Patient.objects.all()[0].name
			patient = get_object_or_404(Patient, name=patientName)
			caregiver = []
			caregiverNames = form.cleaned_data['caregivers']
			for caregiverName in caregiverNames:
				caregiver.append(get_object_or_404(Caregiver, name = caregiverName))
			newGoal = Goal.objects.create(name = name, 
										  notes = notes, 
										  active = active, 
										  patient = patient,
										  data_type = data_type,
										  )

			for c in caregiver:
				newGoal.caregivers.add(c)
			return HttpResponseRedirect('')
	else:
		form = AddGoalForm()



	latest_goals = Goal.objects.order_by('name')
	actions = Action.objects.all()

	goals_context = []
	charts = []
	divs = []
	for g in latest_goals:
		goal = get_object_or_404( Goal, name=g.name)
		this_goal = {}
		this_goal['chart']=[]
		this_goal['div']=[]
		this_goal['goal']=goal


		recent_status_updates = StatusUpdate.objects.filter(goal = goal).order_by('-pub_time')
		goalChart_data = DataPool(
			series = [
				{'options': {
					'source' : recent_status_updates},
					'terms' : [
						('pub_time', lambda d: time.mktime(d.timetuple())),
						'data_value',
						]}
				]
			)

		goalChart = Chart(
			datasource = goalChart_data,
			series_options = [{
				'options':{
	                'type': 'line',
	                'stacking': False},
	            'terms':{
	                'pub_time': [
	                'data_value']}
	         	}],
	         	chart_options = 
	         		{'title': {
	                   'text': goal.name},
	               'xAxis': {
	                    'title': {
	                       'text': 'Date'}
	                       }
	                },
				x_sortf_mapf_mts=(None, lambda i: datetime.datetime.fromtimestamp(i).strftime("%m/%d/%y"), False)
			)

		
		charts.append(goalChart)
		divs.append("goal_chart"+str(goal.id))
		goals_context.append(this_goal)

	
	if len(latest_goals)>0:
		div_string=divs[0]
	for i in range(1,len(latest_goals)):
		div_string=div_string+','+'goal_chart'+str(latest_goals[i].id)
	# div_string = str(divs).strip('[]')

	#end try to add graphs
	# context = {'latest_goals' : latest_goals,
	# 			'actions' : actions,
	# 			'AddGoalForm' : AddGoalForm,
	# 			'goalChart' : goalChart_context,
	# 			'goalChart_div':goalChartDiv
	# 			}

	patients = Patient.objects.all()
	patient = patients[0]
	pic = patient.photo.name.split("/")[-1]

	context = {'goals_context' : goals_context,
				'charts' : charts,
				'divs' : div_string,
				'actions' : actions,
				'AddGoalForm' : AddGoalForm,
				'patient': patient,
				'pic': pic,
				}
	return render(request, 'gk/Home.html', context)



def goal(request, goal_name):
	if (request.method == 'POST'):
		if ('statQuant' in request.POST):
			form = AddQuantStatusForm(request.POST)
			if form.is_valid():
				status = form.cleaned_data['notes']
				data_value = form.cleaned_data['data_Value']
				pub_time = datetime.datetime.now()
				reporting_caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
				goal = get_object_or_404( Goal, name=goal_name)
				NEW_STATUS = StatusUpdate.objects.create(goal=goal,
														 data_value=data_value,
														 pub_time=pub_time,
														 reporting_caregiver=reporting_caregiver,
														 status=status,
														 )
				return HttpResponseRedirect('')

		elif ('statQual' in request.POST):
			form = AddQualStatusForm(request.POST)
			if form.is_valid():
				status = form.cleaned_data['notes']
				data_value = form.cleaned_data['data_Value']
				pub_time = datetime.datetime.now()
				reporting_caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
				goal = get_object_or_404( Goal, name=goal_name)
				NEW_STATUS = StatusUpdate.objects.create(goal=goal,
														 data_value=data_value,
														 pub_time=pub_time,
														 reporting_caregiver=reporting_caregiver,
														 status=status,
														 )
				return HttpResponseRedirect('')
		
		elif ('act' in request.POST):
			form = AddActionForm_GoalPage(request.POST)
			if form.is_valid():
				goal = get_object_or_404( Goal, name=goal_name)
				name = form.cleaned_data['action']
				deadline = form.cleaned_data['due_Date']
				caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
				completed = False
				NEW_ACTION = Action.objects.create(goal = goal, 
												   name = name, 
												   deadline=deadline, 
												   caregiver=caregiver,
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
		form1 = AddActionForm_GoalPage()
		form2 = AddQuantStatusForm()
		form3 = AddQualStatusForm()



	goal = get_object_or_404( Goal, name=goal_name)
	actions = Action.objects.filter(goal = goal)
	completed_actions = [a for a in actions if a.completed]
	pending_actions = [a for a in actions if not a.completed]
	recent_status_updates = StatusUpdate.objects.filter(goal = goal).order_by('-pub_time')
	caregivers = Caregiver.objects.filter(goal = goal)
	qualDict = {0:'Worse',
				1:'Same',
				2:'Better'}


	goalChart_data = DataPool(
		series = [
			{'options': {
				'source' : recent_status_updates},
				'terms' : [
					('pub_time', lambda d: time.mktime(d.timetuple())),
					'data_value',
					]}
			]
		)

	goalChart = Chart(
		datasource = goalChart_data,
		series_options = [{
			'options':{
                'type': 'line',
                'stacking': False},
            'terms':{
                'pub_time': [
                'data_value']}
         	}],
         	chart_options = 
         		{'title': {
                   'text': goal.name},
               'xAxis': {
                    'title': {
                       'text': 'Date'}
                       }
                },
			x_sortf_mapf_mts=(None, lambda i: datetime.datetime.fromtimestamp(i).strftime("%m/%d/%y"), False)
		)




	context = {'goal' : goal,
			   'actions' : actions,
			   'pending_actions' : pending_actions,
			   'completed_actions' : completed_actions,
			   'recent_status_updates' : recent_status_updates,
			   'caregivers' : caregivers,
			   'qualDict' : qualDict,
			   'AddActionForm_GoalPage' : AddActionForm_GoalPage,
			   'AddQuantStatusForm' : AddQuantStatusForm,
			   'AddQualStatusForm' : AddQualStatusForm,
			   'goalChart' : goalChart,
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
				caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
				completed = False
				NEW_ACTION = Action.objects.create(goal = goal, 
												   name = name, 
												   deadline=deadline, 
												   caregiver=caregiver,
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

def caregiverChoices():
	caregiver_choices = []
	for c in Caregiver.objects.all():
		caregiver_choices.append((c.name, c))
	return caregiver_choices

class AddGoalForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(AddGoalForm, self).__init__(*args, **kwargs)
		self.fields['caregivers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
				choices=caregiverChoices() )
	type_choices = [('0', u'Better/Same/Worse'), 
					('1', u'Number Value'),
					]
	
	goal_Name = forms.CharField(max_length = 30)
	Type = forms.ChoiceField(type_choices)
	Description = forms.CharField()
	#caregivers = forms.MultipleChoiceField(caregiver_choices)

class AddContactForm(forms.Form):
	contact_Name = forms.CharField()
	Role = forms.CharField()
	Email = forms.EmailField()
	Phone = forms.CharField()


def goalChoices():
	goal_choices = []
	for g in Goal.objects.all():
		goal_choices.append((g.name, g))
	return goal_choices

class AddActionForm_ActionPage(forms.Form):
	def __init__(self, *args, **kwargs):
		super(AddActionForm_ActionPage, self).__init__(*args, **kwargs)
		self.fields['goal'] = forms.ChoiceField(choices=goalChoices())
		self.fields['action'] = forms.CharField(max_length=32)
		self.fields['due_Date'] = forms.DateField(widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
	
	

class AddActionForm_GoalPage(forms.Form):
	action = forms.CharField(max_length=32)
	due_Date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

class AddQuantStatusForm(forms.Form):
	data_Value = forms.IntegerField()
	notes = forms.CharField()

class AddQualStatusForm(forms.Form):
	choices = [('2', u'Better'),
			   ('1', u'Same'),
			   ('0', u'Worse'), 
			   ]
	data_Value = forms.ChoiceField(choices)
	notes = forms.CharField()

class complete_button(forms.Form):
	pass










