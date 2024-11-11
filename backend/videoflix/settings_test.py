from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "test_db.sqlite3",
    }
}
RQ_QUEUES = {
    'default': {
        'USE_IN_MEMORY_BACKEND': True,
        'HOST': 'localhost',
        'PORT': 6379,
    },
    'low': {
        'USE_IN_MEMORY_BACKEND': True,
        'HOST': 'localhost',
        'PORT': 6379,
    },
    'high': {
        'USE_IN_MEMORY_BACKEND': True,
        'HOST': 'localhost',
        'PORT': 6379,
    },
}
