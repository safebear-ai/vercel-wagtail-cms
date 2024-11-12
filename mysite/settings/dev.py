from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "2(-_x@7e09)^!=dsi^_1j=tchz)ecy2q1)7rti4*r**p4%ma#&"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [  # noqa
    "django_sass",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = True

try:
    from .local import *  # noqa
except ImportError:
    pass
