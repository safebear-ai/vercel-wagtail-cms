# wsgi.py
```py
import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safebear_cms.settings.prod")

application: WSGIHandler = get_wsgi_application()

app = application
```

## Poetry cli
`poetry export -f requirements.txt --output requirements.txt`