
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


POSTGRESQL = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'DommunDb',
            'USER': 'postgres',
            'PASSWORD': 'Juan2020.',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
