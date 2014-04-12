from settings.common import *
import os


DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'database', 'db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console'],
        },
        'weditor': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
    }
}
