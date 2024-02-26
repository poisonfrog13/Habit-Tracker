"""
Use this module to specify the values of any settings which should
be used in development.

To do this, simply declare the values as you would in a regular Django
settings.py file. The values given here can be combined with, or overload values
given in the base settings module.

It is recommended that you are familliar with server.settings.base in order to
understand what values you need to change for your project.

Combined example:

ALLOWED_HOSTS += [
    "172.168.4.0"
]

Overload example:

DEBUG = False
"""

# Import base settings
from server.settings.develop import *  # noqa: F403

# Identify the settings module
SETTINGS_MODULE = "PRODUCTION"

# Define your development settings here
ALLOWED_HOSTS += [  # noqa: F405
    "*",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEVELOP = False

print(
    f"DJANGO SETTINGS | {SETTINGS_MODULE=} | {DEVELOP=}, {DEBUG=}"  # noqa: F405
)
