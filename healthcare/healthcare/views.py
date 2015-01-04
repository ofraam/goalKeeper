# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from gk.models import Caregiver, Patient
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

@login_required
def logs(request):
    number_logs = request.GET.get('latest')    

    with open(settings.BASE_DIR+"/logfile", 'rb') as f:
        lines = f.readlines()
        if number_logs is not None:
            lines = lines[-number_logs:]
        return HttpResponse("<br/>".join(lines))    

def show_login(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    else:
        return render(request, 'healthcare/login.html')    

@login_required
def home(request):
    user = request.user
    patient_caregiver, type = get_patient_caregiver(user)   
    if type=="patient":
        patient = patient_caregiver
        caregiver = None
    else:
        patient = None
        caregiver = patient_caregiver
    #return render(request, 'healthcare/home.html', {"user_type": type, "patient": patient, "caregiver": caregiver})
    return redirect('/goalkeeper/')


def try_get_caregiver(user):
    try:
        caregiver = Caregiver.objects.get(user=user)
        if caregiver:
            return caregiver
    except:
        return None

def try_get_patient(user):
    try:
        patient = Patient.objects.get(user=user)
        if patient:
            return patient
    except:
        return None

def get_patient_caregiver(user):
    patient = try_get_patient(user)
    if patient:
        return patient, "patient"
    
    caregiver = try_get_caregiver(user)
    if caregiver:
        return caregiver, "caregiver"

    return None, None

def login_handler(request):
    username = request.POST['email']
    password = request.POST['password']    
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/home/')
        else:
            return render(request, 'healthcare/login.html', {"message": "Sorry, there was a problem logging you in."})
    else:
        return render(request, 'healthcare/login.html', {"message": "Sorry, there was a problem with your username or password."})

def logout_handler(request):
    logout(request)
    return render(request, 'healthcare/login.html')
