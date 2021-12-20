import os

# This defines the base dir for all relative imports for our project, put the file in your root folder so the
# base_dir points to the root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# According to your data file, you can change the engine, like mysql, postgresql, mongodb etc make sure your data is
# directly placed in the same folder as this file, if it is not, please direct the 'NAME' field to its actual path.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Since we only have one app which we use
INSTALLED_APPS = ("app",
    "django.contrib.admin", 
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles"
)

# Write a random secret key here
SECRET_KEY = "not secret"

ALLOWED_HOSTS = ["localhost"]
ROOT_URLCONF = "app.urls"
DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

OPTIONS = {
    "context_processors": "django.contrib.messages.context_processors.messages"
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
