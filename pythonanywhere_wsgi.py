# This file contains the WSGI configuration required to serve up your
# web application at http://Nalisa13.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import os
import sys

# Add your project directory to the sys.path
path = '/home/Nalisa13/momenta'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'event_system.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

application = StaticFilesHandler(get_wsgi_application())