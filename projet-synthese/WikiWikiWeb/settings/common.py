import django.conf
import os

DEBUG = False
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False

SECRET_KEY = 's0y^h+^*n=ci-8l1spnka0y&9n6o&lt9me8c-g21gfi+uflg93'

ADMINS = (
    ('Freaxmind', 'freaxmind@freaxmind.pro'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = True
USE_L10N = True
USE_TZ = False

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__ ), '..'))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'public/media')
STATIC_ROOT = os.path.join(SITE_ROOT, 'public/static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_URL = '/connecte'
LOGOUT_URL = '/deconnecte'
LOGIN_REDIRECT_URL = '/accueil'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'urls'

CAPTCHA_LENGTH=6
CAPTCHA_FONT_SIZE=35
CAPTCHA_BACKGROUND_COLOR="#000000"
CAPTCHA_FOREGROUND_COLOR="#FFFFFF"

ANTISPAM_LIMIT = 3
ANTISPAM_SESSION = 'antispam_counter'
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
X_FRAME_OPTIONS = 'DENY'

ARTICLES_PER_USER=3
SEARCH_SESSION = 'search_session'

STATICFILES_DIRS = (

)
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'weditor', 'templates'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = django.conf.global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'captcha', # apt-get install python-imaging / pip install django-simple-captcha
    'social.apps.django_app.default', # pip install django-social-auth / syncdb
    'weditor',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOpenId',
    'social.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
  )
