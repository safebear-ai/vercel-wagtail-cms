# Readme

## wsgi.py
```py
import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safebear_cms.settings.prod")

application: WSGIHandler = get_wsgi_application()

app = application
```
---
## Poetry cli
```
poetry export -f requirements.txt --output requirements.txt
```
---
## Build the Sass:

``` 
python manage.py sass -g safebear_cms/static/safebear_cms/src/custom.scss safebear_cms/static/safebear_cms/css/
```

   To build the Sass automatically whenever you change a file, add the --watch
   option and run it in a separate terminal. To build a compressed/minified
   production version, add the -t compressed option. For more options, see
   django-sass.

---
## Tasks

This project uses a `Taskfile` to automate key steps for managing and deploying a Django application with Wagtail.

### `install`
Installs dependencies and sets up the environment:
- Activates Poetry virtual environment.
- Installs Python and npm dependencies.
- Exports `requirements.txt`.
- Pulls environment variables from Vercel.

### `collectstatic`
Collects static files for production:
- Runs `python manage.py collectstatic --noinput`.

### `migrate`
Handles database migrations:
- Runs `makemigrations` and `migrate`.

### `local`
Starts the local Django development server:
- Runs `python manage.py runserver`.

### `build`
Prepares the app for deployment by running:
1. `install`
2. `collectstatic`
3. `migrate`

### `deploy-preview`
Builds and deploys the app preview to Vercel:
- Runs `build`.
- Deploys using `vercel`.

### `deploy-local`
Builds and runs the app locally:
- Runs `build` followed by `local`.

### `deploy-prod`
Builds and runs the app prod to Vercel:
- Runs `build` followed by `local`.

---

## Usage

Run tasks using:

```bash
task <task-name>
```

### Examples
- Install dependencies:
  ```bash
  task install
  ```
- Deploy to Vercel:
  ```bash
  task deploy
  ```

## Documentation links

- To customize the content, design, and features of the site see [Wagtail CRX](https://discord.com/channels/@me/1242407406638600305/1318208665626480670).

- For deeper customization of backend code see [Wagtail](https://discord.com/channels/@me/1242407406638600305/1318208665626480670) and [Django](https://discord.com/channels/@me/1242407406638600305/1318208665626480670).

- For HTML template design see [Bootstrap](https://discord.com/channels/@me/1242407406638600305/1318208665626480670).