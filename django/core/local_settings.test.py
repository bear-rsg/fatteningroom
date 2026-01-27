"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'u6n(9&8g-3=6d1#jyp^#))you-h&y^-5y7*&hu)cpxzeu_7#j+'

DEBUG = True

ALLOWED_HOSTS = ['*']

MAIN_CONTACT_EMAIL = 'bear-rsg@contacts.bham.ac.uk'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'fatteningroom.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'fatteningroom_TEST.sqlite3'),
        },
    }
}


# Email
DEFAULT_FROM_EMAIL = 'anemailaddress@bham.ac.uk'
NOTIFICATION_EMAIL = 'anemailaddress@bham.ac.uk'
if DEBUG is True:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_USE_TLS = False
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'hostnamehere'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = 'anemailaddress@bham.ac.uk'
