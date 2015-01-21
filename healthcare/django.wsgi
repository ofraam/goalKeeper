import os
import sys

path = "/var/www/html/goalkeeper/healthcare"
if path not in sys.path:
	sys.path.append(path)

os.environ['PYTHON_EGG_CACHE'] = '/var/www/html/goalkeeper/healthcare.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'healthcare.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
