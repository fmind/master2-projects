from django.core.wsgi import get_wsgi_application
import os, sys

_PROJECT_DIR = '/var/www/WikiWikiWeb/'

if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")

application = get_wsgi_application()
