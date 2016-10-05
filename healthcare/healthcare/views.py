# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from gk.models import Caregiver, Patient
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''

    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser

@login_required
def logs(request):
    if request.user.is_authenticated() and request.user.is_staff:
        number_logs = request.GET.get('latest')    

        with open(settings.BASE_DIR+"/logfile", 'rb') as f:
            lines = f.readlines()
            if number_logs is not None:
                lines = lines[-number_logs:]
            return HttpResponse("<br/>".join(lines))    
    else:
        return render(request, 'login.html', {"message": "Sorry, you don't have permission to view that page."})

def show_login(request):
    if request.user.is_authenticated():
        return redirect('gk:home')
    else:
        return render(request, 'login.html')    

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
    return redirect('gk:home')


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
        return patient, "patient", ""
    
    caregiver = try_get_caregiver(user)
    if caregiver:
        return caregiver, "caregiver", caregiver.role

    return None, None

def login_handler(request):
    username = request.POST['email']
    password = request.POST['password']    
    #timezoneUser = request.POST['timezone']
    
    user = authenticate(username=username, password=password)
    #if timezoneUser=='PDT':
	#timezone.activate(pytz.timezone('US/Pacific-New'))
#    else:
#	timezone.activate(pytz.timezone('US/Eastern'))
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('gk:home')
        else:
            return render(request, 'login.html', {"message": "Sorry, there was a problem logging you in.","islogin": "islogin"})
    else:
        return render(request, 'login.html', {"message": "Sorry, there was a problem with your username or password.","islogin": "islogin"})

def logout_handler(request):
    logout(request)
    return render(request, 'login.html')
