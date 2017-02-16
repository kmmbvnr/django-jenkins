import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'test_app.urls'
SECRET_KEY = 'nokey'
MIDDLEWARE_CLASSES = ()

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

PROJECT_APPS = (
    'django.contrib.sessions',  # just to ensure that dotted apps test works
    'django_jenkins',
    'tests.test_app',
    'tests.test_app_dirs',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
) + PROJECT_APPS


DATABASE_ENGINE = 'sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        }
}

SOUTH_MIGRATION_MODULES = {
    'test_app': 'test_app.south_migrations',
}

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_flake8',
)

COVERAGE_EXCLUDES = ['tests.test_app.not_for_coverage', ]
COVERAGE_EXCLUDES_FOLDERS = [os.path.join(PROJECT_ROOT, 'test_app_dirs/not_for_coverage/'), ]

# JSHINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/js/test.js')]
# CSSLINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/css/test.css')]

PYLINT_LOAD_PLUGIN = (
    'pylint_django',
)

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static/'),
]

STATIC_URL = '/media/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
