import sys
import os

# add up one level dir into sys path
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
WWW_DIR = os.path.abspath(os.path.join(PARENT_DIR, '..'))
for path in [PARENT_DIR, WWW_DIR]:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'lisa.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
