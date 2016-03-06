"""
WSGI config for Portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Portal.settings")

base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

application = get_wsgi_application()
"""

import site

# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/home/byld/scripting101/.env/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/byld/scripting101/scripting-challenge-byld')
sys.path.append('/home/byld/scripting101/scripting-challenge-byld/Portal')

#os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/byld/scripting101/.env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))


from django.core.handlers.wsgi import WSGIHandler

#os.environ['DJANGO_SETTINGS_MODULE'] = 'PROJECT_NAME.subdomain1_settings' # or PROJECT_NAME.subdomain2_settings
application = WSGIHandler()

######################33

import os
import sys

from os.path import abspath, dirname, join

# This is /srv/django/yoursite
PROJECT_PATH=abspath(join(dirname(__file__), "."))

import site
import os

# Assume virtualenv is in relative subdirectory "venv" to the project root
vepath = PROJECT_PATH+'/home/byld/scripting101/.env/lib/python2.7/site-packages'

prev_sys_path = list(sys.path)
# add the site-packages of our virtualenv as a site dir
site.addsitedir(vepath)


# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# import from down here to pull in possible virtualenv django install
from django.core.handlers.wsgi import WSGIHandler
#os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
application = WSGIHandler()
"""
