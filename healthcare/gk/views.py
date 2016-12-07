from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from gk.models import *
from django import forms
from chartit import DataPool, Chart
import datetime
import time
from django.contrib.auth.decorators import login_required
from healthcare.views import get_patient_caregiver
from django.utils import timezone
from django.http import JsonResponse
from django.db import connections

import pytz
import logging

from healthcare.views import mobileBrowser

logger = logging.getLogger(__name__)
# timezone.deactivate()
timezone.activate(pytz.timezone('US/Eastern'))


# ctivate(pytz.timezone(tzname))utililty used to write out to the log file
# logs have the tab-delimited format of:
# Timestamp	UserType	UserID	PatientID	Action	ActionID
# the Django logging protocol adds in and formats time already,
# so we provide a tab-delimited string of the remaining parameters
def write_to_log(user_type, user_id, patient_id, action, action_id):
    logger.info("\t".join(map(str, [user_type, user_id, patient_id, action, action_id])))


# this is a helper function to check if we have a current user,
# identify if that user is a caregiver or patient,
# and redirect to the login page if they are not logged in
def check_user(request):
    viewer, viewer_type, viewer_role = get_patient_caregiver(request.user)

    # if we're not logged in properly
    if not request.user.is_authenticated() or viewer_type == None or viewer == None:
        # throw an error message
        return redirect('healthcare:home')

    return (viewer, viewer_type, viewer_role)


# this is a helper function to check if a given viewer
# has permission to view a given patient. This is based on a
# caregiver having permission on a patient, or the viewer being
# the patient themselves
def user_has_permission(request, viewer, viewer_type, patient):
    # checks if we're a caregiver who doesn't have access to this page
    if viewer_type == "caregiver" and not patient.caregiver.filter(id=viewer.id).exists():
        return render(request, "gk/Error.html", {'message': "Sorry, you don't have permission to view that patient.",
                                                 'viewer_name': viewer.name,})
    elif viewer_type == "patient" and viewer != patient:
        return render(request, "gk/Error.html", {'message': "Sorry, you don't have permission to view other patients.",
                                                 'viewer_name': viewer.name,})

    return True


@login_required
def landing_page(request):
    print check_user(request)
    viewer, viewer_type, viewer_role = check_user(request)

    write_to_log(viewer_type, viewer.id, '', 'landing_page', '')

    # if we're a patient
    if viewer_type == "patient":
        return redirect('gk:home', user_id=str(viewer.id))
    # otherwise, if we're a caregiver
    elif viewer_type == "caregiver":
        patients = Patient.objects.filter(caregiver=viewer)
        context = {
            'patients': patients,
            'viewer_role': viewer_role,
            'viewer_name': viewer.name
        }
        return render(request, 'gk/Landing.html', context)


@login_required
def edit_status(request, goal_id):
    print "editing"


# Create your views here.
@login_required
def home(request, user_id):
    viewer, viewer_type, viewer_role = check_user(request)

    patient = get_object_or_404(Patient, id=user_id)
    valid = user_has_permission(request, viewer, viewer_type, patient)

    # if invalid, render the error page
    if valid != True:
        return valid

    errors = None
    non_field_errors = None

    if (request.method == 'POST'):
        form = AddGoalForm(request.POST, patient=patient)
        if form.is_valid():
            name = form.cleaned_data['goal_Name']
            data_type = form.cleaned_data['Type']
            notes = form.cleaned_data['Description']
            active = True
            patientName = patient.name
            caregiver = []
            caregiverNames = form.cleaned_data['caregivers']
            for caregiverName in caregiverNames:
                caregiver.append(get_object_or_404(Caregiver, name=caregiverName))
            newGoal = Goal.objects.create(name=name,
                                          notes=notes,
                                          active=active,
                                          patient=patient,
                                          data_type=data_type,
                                          )
            for c in caregiver:
                newGoal.caregivers.add(c)

            write_to_log(viewer_type, viewer.id, user_id, 'create_new_goal', newGoal.id)

        # return HttpResponseRedirect('')
        else:
            errors = form.errors
            non_field_errors = form.non_field_errors
    else:
        form = AddGoalForm(patient=patient)

    latest_goals = Goal.objects.filter(patient=patient, caregivers__id__exact=viewer.id).order_by('name')
    actions = Action.objects.filter(goal__patient=patient).all()

    goals_context = []
    charts = []
    divs = []
    for g in latest_goals:
        goal = get_object_or_404(Goal, id=g.id)
        this_goal = {}
        this_goal['chart'] = []
        this_goal['div'] = []
        this_goal['goal'] = goal

        recent_status_updates = StatusUpdate.objects.filter(goal=goal).order_by('-pub_time')
        goalChart_data = DataPool(
            series=[
                {'options': {
                    'source': recent_status_updates},
                    'terms': [
                        ('pub_time', lambda d: time.mktime(d.timetuple())),
                        'data_value',
                    ]}
            ]
        )

        goalChart = Chart(
            datasource=goalChart_data,
            series_options=[{
                'options': {
                    'type': 'line',
                    'stacking': False},
                'terms': {
                    'pub_time': [
                        'data_value']}
            }],
            chart_options=
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
        divs.append("goal_chart" + str(goal.id))

        goals_context.append(this_goal)

    active_goals = [x for x in goals_context if x['goal'].active]
    inactive_goals = [x for x in goals_context if not x['goal'].active]

    if len(latest_goals) > 0:
        div_string = divs[0]
    else:
        div_string = ""
    for i in range(1, len(latest_goals)):
        div_string = div_string + ',' + 'goal_chart' + str(latest_goals[i].id)
    # div_string = str(divs).strip('[]')

    # end try to add graphs
    # context = {'latest_goals' : latest_goals,
    # 			'actions' : actions,
    # 			'AddGoalForm' : AddGoalForm,
    # 			'goalChart' : goalChart_context,
    # 			'goalChart_div':goalChartDiv
    # 			}

    pic = patient.photo.name.split("/")[-1]
    context = {'goals_context': active_goals,
               'inactive_goals_context': inactive_goals,
               'charts': charts,
               'divs': div_string,
               'actions': actions,
               'AddGoalForm': form,
               'patient': patient,
               'pic': pic,
               'viewer_name': viewer.name,
               'viewer_type': viewer_type,
               'viewer_role': viewer_role,
               'errors': errors,
               'non_field_errors': non_field_errors
               }

    write_to_log(viewer_type, viewer.id, user_id, 'patient', '')

    if mobileBrowser(request):
        # t = loader.get_template('gk/m_home.html')
        return render(request, 'gk/m_home.html', context)
    else:
        # t = loader.get_template('gk/Home.html')
        return render(request, 'gk/Home.html', context)

        # return HttpResponse(t.render(context))


@login_required
def goal(request, goal_id):
    viewer, viewer_type, viewer_role = check_user(request)
    if ((viewer.id == 9) | (viewer.id == 8)):
        timezone.activate(pytz.timezone('US/Eastern'))
    else:
        timezone.activate(pytz.timezone('US/Pacific-New'))
    goal = get_object_or_404(Goal, id=goal_id)
    patient = goal.patient
    valid = user_has_permission(request, viewer, viewer_type, patient)

    errors = None
    non_field_errors = None

    # if invalid, render the error page
    if valid != True:
        return valid

    if (request.method == 'POST'):
        # you must be a caregiver to be able to assign goals/updates
        if viewer_type != "caregiver":
            return render(request, "gk/Error.html",
                          {'message': "Sorry, you must be a caregiver to create updates", 'name': viewer.name,})

        if ('statQuant' in request.POST):
            form = AddQuantStatusForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['notes']
                data_value = form.cleaned_data['data_Value']
                # pub_time = datetime.datetime.now()
                pub_time = timezone.now()
                # reporting_caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
                reporting_caregiver = viewer
                NEW_STATUS = StatusUpdate.objects.create(goal=goal,
                                                         data_value=data_value,
                                                         pub_time=pub_time,
                                                         reporting_caregiver=reporting_caregiver,
                                                         status=status,
                                                         )

                write_to_log(viewer_type, viewer.id, patient.id, 'new_quantitative_status', NEW_STATUS.id)

            # return HttpResponseRedirect('')
            else:
                errors = form.errors
                non_field_errors = form.non_field_errors

        elif ('statQual' in request.POST):
            form = AddQualStatusForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['notes']
                data_value = form.cleaned_data['data_Value']
                pub_time = datetime.datetime.now()
                # reporting_caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
                reporting_caregiver = viewer
                NEW_STATUS = StatusUpdate.objects.create(goal=goal,
                                                         data_value=data_value,
                                                         pub_time=pub_time,
                                                         reporting_caregiver=reporting_caregiver,
                                                         status=status,
                                                         )
                write_to_log(viewer_type, viewer.id, patient.id, 'new_qualitative_status', NEW_STATUS.id)

            # return HttpResponseRedirect('')
            else:
                errors = form.errors
                non_field_errors = form.non_field_errors

        elif ('act' in request.POST):
            form = AddActionForm_GoalPage(request.POST)
            if form.is_valid():
                name = form.cleaned_data['action']
                notes = form.cleaned_data['notes']
                deadline = form.cleaned_data['due_Date']
                # caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
                caregiver = viewer
                completed = False
                NEW_ACTION = Action.objects.create(goal=goal,
                                                   name=name,
                                                   notes=notes,
                                                   deadline=deadline,
                                                   caregiver=caregiver,
                                                   completed=completed,
                                                   )
                write_to_log(viewer_type, viewer.id, patient.id, 'new_action', NEW_ACTION.id)

            # return HttpResponseRedirect('')
            else:
                errors = form.errors
                non_field_errors = form.non_field_errors

        elif ('Complete' in request.POST):
            action = get_object_or_404(Action, id=request.POST.get('actionName', False))
            action.completed = True
            action.save()

            write_to_log(viewer_type, viewer.id, patient.id, 'completed_action', action.id)

        # return HttpResponseRedirect('')


        elif ('remove' in request.POST):
            action = get_object_or_404(Action, id=request.POST.get('actionName', False))
            action.delete()

            write_to_log(viewer_type, viewer.id, patient.id, 'removed_action', action.id)

        # return HttpResponseRedirect('')

        elif ('updateStatus' in request.POST):
            status = get_object_or_404(StatusUpdate, id=request.POST.get('statusID', False))

            form = UpdateQuantStatusForm(request.POST)
            if form.is_valid():
                status_text = form.cleaned_data['notes']
                data_value = form.cleaned_data['data_Value']
                status_time = form.cleaned_data['pub_time']

                status.status = status_text
                status.data_value = data_value
                status.pub_time = status_time

                status.save()
                write_to_log(viewer_type, viewer.id, patient.id, 'edit_status_update', status.id)

            else:
                errors = form.errors
                non_field_errors = form.non_field_errors

        elif ('updateGoal' in request.POST):
            goal_form = UpdateGoalForm(request.POST, patient=patient)
            if goal_form.is_valid():
                new_name = goal_form.cleaned_data['name']
                new_notes = goal_form.cleaned_data['notes']
                new_active = goal_form.cleaned_data['active']

                caregiver = []
                caregiverIds = goal_form.cleaned_data['caregivers']
                for caregiverId in caregiverIds:
                    caregiver.append(get_object_or_404(Caregiver, id=caregiverId))

                for c in goal.caregivers.all():
                    if c.id not in caregiverIds:
                        goal.caregivers.remove(c)
                for c in caregiver:
                    goal.caregivers.add(c)

                goal.name = new_name
                goal.notes = new_notes
                goal.active = new_active

                goal.save()
                write_to_log(viewer_type, viewer.id, patient.id, 'edit__goal', goal.id)

            else:

                errors = goal_form.errors
                non_field_errors = goal_form.non_field_errors

    else:
        form1 = UpdateGoalForm(patient=patient)
        # form4 = AddActionForm_GoalPage()
        form2 = AddQuantStatusForm()
        form3 = AddQualStatusForm()

    actions = Action.objects.filter(goal=goal)
    completed_actions = [a for a in actions if a.completed]
    pending_actions = [a for a in actions if not a.completed]

    recent_status_updates = StatusUpdate.objects.filter(goal=goal).order_by('-pub_time')
    status_update_forms = [AddQuantStatusForm(x) for x in recent_status_updates]
    status_updates_and_forms = [{'form': status_update_forms[i], 'status_data': recent_status_updates[i]} for i in
                                range(len(recent_status_updates))]

    caregivers = Caregiver.objects.filter(goal=goal)
    all_caregivers = patient.caregiver.all()
    qualDict = {0: 'Worse',
                1: 'Same',
                2: 'Better'}


    context = {'goal': goal,
               'actions': actions,
               'pending_actions': pending_actions,
               'completed_actions': completed_actions,
               'recent_status_updates': status_updates_and_forms,
               'caregivers': caregivers,
               'all_caregivers': all_caregivers,
               'qualDict': qualDict,
               'AddActionForm_GoalPage': AddActionForm_GoalPage,
               'AddQuantStatusForm': AddQuantStatusForm,
               'AddQualStatusForm': AddQualStatusForm,
               'goal_id' : goal_id,
               'viewer_name': viewer.name,
               'viewer_role': viewer_role,
               'viewer_type': viewer_type,
               'patient': patient,
               'errors': errors,
               'non_field_errors': non_field_errors
               }

    write_to_log(viewer_type, viewer.id, patient.id, 'goal', goal_id)
    return render(request, 'gk/Goal.html', context)


@login_required
def goal_over_time(request, goal_id):
    data = StatusUpdate.objects.filter(goal=goal_id).order_by('-pub_time').extra(select={
        'day': connections[StatusUpdate.objects.db].ops.date_trunc_sql('day',
                                                                        'pub_time')}).values('day', 'data_value')

    print(data)
    return JsonResponse(list(data), safe=False)


@login_required
def action(request, patient_id):
    viewer, viewer_type, viewer_role = check_user(request)
    # goal = get_object_or_404( Goal, name=goal_name)
    # goal = Goal.objects.get(id=3)
    patient = get_object_or_404(Patient, id=patient_id)
    valid = user_has_permission(request, viewer, viewer_type, patient)

    errors = None
    non_field_errors = None

    # if invalid, render the error page
    if valid != True:
        return valid

    if (request.method == 'POST'):
        # you must be a caregiver to be able to assign actions
        if viewer_type != "caregiver":
            return render(request, "gk/Error.html",
                          {'message': "Sorry, you must be a caregiver to create actions", 'name': viewer.name,})

        if ('actionForm' in request.POST):
            form = AddActionForm_ActionPage(request.POST, patient=patient)
            if form.is_valid():
                goal_name = form.cleaned_data['goal']
                goal = get_object_or_404(Goal, name=goal_name)
                name = form.cleaned_data['action']
                notes = form.cleaned_data['notes']
                deadline = form.cleaned_data['due_Date']
                # caregiver = get_object_or_404(Caregiver, name = Caregiver.objects.all()[0].name)
                caregiver = viewer
                completed = False
                NEW_ACTION = Action.objects.create(goal=goal,
                                                   name=name,
                                                   notes=notes,
                                                   deadline=deadline,
                                                   caregiver=caregiver,
                                                   completed=completed,
                                                   )

                write_to_log(viewer_type, viewer.id, patient.id, 'new_action', NEW_ACTION.id)
            else:
                errors = form.errors
                non_field_errors = form.non_field_errors

        elif ('complete' in request.POST):
            action = get_object_or_404(Action, id=request.POST.get('actionName', False))
            action.completed = True
            action.save()

            write_to_log(viewer_type, viewer.id, patient.id, 'completed_action', action.id)

        elif ('remove' in request.POST):
            action = get_object_or_404(Action, id=request.POST.get('actionName', False))
            action.delete()

            write_to_log(viewer_type, viewer.id, patient.id, 'removed_action', action.id)

    form = AddActionForm_ActionPage(patient=patient)

    actions = Action.objects.filter(goal__patient=patient, goal__caregivers__id__exact=viewer.id).order_by('-deadline')
    completed_actions = [a for a in actions if a.completed]
    pending_actions = [a for a in actions if not a.completed]
    context = {'actions': actions,
               'pending_actions': pending_actions,
               'completed_actions': completed_actions,
               'AddActionForm_ActionPage': form,
               'name': viewer.name,
               'viewer_role': viewer_role,
               'viewer_type': viewer_type,
               'patient': patient,
               'errors': errors,
               'non_field_errors': non_field_errors
               }

    write_to_log(viewer_type, viewer.id, patient.id, 'actions', '')

    if mobileBrowser(request):
        return render(request, 'gk/m_actions.html', context)
    else:
        return render(request, 'gk/actions.html', context)


@login_required
def contacts(request, patient_id):
    viewer, viewer_type, viewer_role = check_user(request)
    # goal = get_object_or_404( Goal, name=goal_name)
    # goal = Goal.objects.get(id=3)
    patient = get_object_or_404(Patient, id=patient_id)
    valid = user_has_permission(request, viewer, viewer_type, patient)

    # if invalid, render the error page
    if valid != True:
        return valid

    errors = None
    non_field_errors = None

    write_to_log(viewer_type, viewer.id, patient.id, 'contactsPage', 'view')
    if (request.method == 'POST'):
        write_to_log(viewer_type, viewer.id, patient.id, 'contacts', 'in if1')
        form = AddContactForm(request.POST)
        if form.is_valid():
            write_to_log(patient.id, patient.id, patient.id, 'contactsOfra', 'in if2')
            name = form.cleaned_data['contact_Name']
            role = form.cleaned_data['Role']
            email = form.cleaned_data['Email']
            phone = form.cleaned_data['Phone']
            NEW_CONTACT = Caregiver.objects.create(name=name,
                                                   role=role,
                                                   email=email,
                                                   phone=phone,
                                                   )

            write_to_log(viewer_type, viewer.id, patient.id, 'contacts', NEW_CONTACT.name)
            patient.caregiver.add(NEW_CONTACT)
            patient.save()
        # return HttpResponseRedirect('')
        else:
            errors = form.errors
            non_field_errors = form.non_field_errors
    else:
        form = AddContactForm()
    caregivers = patient.caregiver.all()
    context = {'caregivers': caregivers,
               'AddContactForm': AddContactForm,
               'patient': patient,
               'errors': errors,
               'viewer_role': viewer_role,
               'viewer_type': viewer_type,
               'non_field_errors': non_field_errors
               }
    write_to_log(viewer_type, viewer.id, patient.id, 'view_contacts', 'contacts')

    if mobileBrowser(request):
        return render(request, 'gk/m_contacts.html', context)
    else:
        return render(request, 'gk/Contacts.html', context)


@login_required
def profile(request, patient_id):
    viewer, viewer_type, viewer_role = check_user(request)
    patient = get_object_or_404(Patient, id=patient_id)
    valid = user_has_permission(request, viewer, viewer_type, patient)

    # if invalid, render the error page
    if valid != True:
        return valid

    if (request.method == 'POST'):
        patient.info = request.POST["patientSummary"]
        patient.name = request.POST["patientName"]
        patient.age = request.POST["patientAge"]
        patient.save()

    updates = StatusUpdate.objects.filter(goal__patient__id=patient.id, goal__caregivers__id__exact=viewer.id).order_by(
        '-pub_time')[:5]
    context = {'patient': patient,
               'viewer_role': viewer_role,
               'viewer_type': viewer_type,
               'updates': updates,
               }
    write_to_log(viewer_type, viewer.id, patient.id, 'view_profile', 'profile')
    return render(request, 'gk/Profile.html', context)


def sample_cg(request):
    ### SAMPLE LOGIN
    user = request.user
    if user_type(user) == 1:
        #### display all of the display logic here
        return None
    else:
        ### we have a doctor
        return None


def user_type(user):
    if user.caregiver:
        return 1
    return 0


############### Form Classes ###############

def caregiverChoices(patient=None):
    if patient is None:
        caregiver_choices = []
        for c in Caregiver.objects.all():
            caregiver_choices.append((c.name, c))
        return caregiver_choices
    else:
        caregiver_choices = []
        for c in patient.caregiver.all():
            caregiver_choices.append((c.name, c))
        return caregiver_choices


def caregiverChoicesIDs(patient=None):
    if patient is None:
        caregiver_choices = []
        for c in Caregiver.objects.all():
            caregiver_choices.append((c.id, c))
        return caregiver_choices
    else:
        caregiver_choices = []
        for c in patient.caregiver.all():
            caregiver_choices.append((c.id, c))
        return caregiver_choices


class AddGoalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient')

        super(AddGoalForm, self).__init__(*args, **kwargs)

        self.fields['caregivers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                              choices=caregiverChoices(patient))

    type_choices = [  # ('0', u'Better/Same/Worse'),
        ('1', u'Number Value'),
    ]

    goal_Name = forms.CharField()
    Type = forms.ChoiceField(type_choices)
    Description = forms.CharField()


# caregivers = forms.MultipleChoiceField(caregiver_choices)

class UpdateGoalForm1(forms.Form):
    type_choices = [  # ('0', u'Better/Same/Worse'),
        ('1', u'Number Value'),
    ]

    goal_Name = forms.CharField()
    Type = forms.ChoiceField(type_choices)
    Description = forms.CharField()


class UpdateGoalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient')
        super(UpdateGoalForm, self).__init__(*args, **kwargs)
        self.fields['caregivers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                              choices=caregiverChoicesIDs(patient))

    name = forms.CharField()
    notes = forms.CharField()
    active = forms.BooleanField(required=False, initial=False)


# caregivers = forms.MultipleChoiceField(caregiver_choices)





def goalChoices(patient=None):
    if patient is None:
        goal_choices = []
        for g in Goal.objects.all():
            goal_choices.append((g.name, g))
        return goal_choices
    else:
        goal_choices = []
        for g in Goal.objects.filter(patient=patient):
            goal_choices.append((g.name, g))
        return goal_choices


class AddContactForm(forms.Form):
    contact_Name = forms.CharField()
    Role = forms.CharField()
    Email = forms.EmailField()
    Phone = forms.CharField()


class AddActionForm_ActionPage(forms.Form):
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient')

        super(AddActionForm_ActionPage, self).__init__(*args, **kwargs)
        self.fields['goal'] = forms.ChoiceField(choices=goalChoices(patient=patient))
        self.fields['action'] = forms.CharField()
        self.fields['notes'] = forms.CharField(required=False)
        self.fields['due_Date'] = forms.DateField(widget=forms.DateInput(attrs=
        {
            'class': 'datepicker'
        }))


class AddActionForm_GoalPage(forms.Form):
    action = forms.CharField()
    notes = forms.CharField(required=False)
    due_Date = forms.DateField(widget=forms.DateInput(attrs=
    {
        'class': 'datepicker'
    }))


class AddQuantStatusForm(forms.Form):
    data_Value = forms.FloatField()
    notes = forms.CharField()
    pub_time = forms.DateTimeField(input_formats=["%m/%d %Y %H:%M"])


class UpdateQuantStatusForm(forms.Form):
    data_Value = forms.FloatField()
    notes = forms.CharField()
    pub_time = forms.DateTimeField(input_formats=["%m/%d %Y %H:%M"])


class AddQualStatusForm(forms.Form):
    choices = [('2', u'Better'),
               ('1', u'Same'),
               ('0', u'Worse'),
               ]
    data_Value = forms.ChoiceField(choices)
    notes = forms.CharField()


class complete_button(forms.Form):
    pass
