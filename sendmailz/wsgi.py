import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sendmailz.settings")

# This should be enough
handler = get_wsgi_application()
