"""
WSGI config for cms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safebear_cms.settings.dev")

application: WSGIHandler = get_wsgi_application()

app = application
# try:
#     from django.core.wsgi import get_wsgi_application
#     application: WSGIHandler = get_wsgi_application()
#     app: WSGIHandler = get_wsgi_application()
# except ImportError:
#     pass
