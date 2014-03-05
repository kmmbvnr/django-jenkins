import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'test_app.urls'
SECRET_KEY = 'nokey'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

PROJECT_APPS = (
    'django.contrib.sessions',  # just to ensure that dotted apps test works
    'django_jenkins',
    'test_app',
    'test_app_dirs',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
) + PROJECT_APPS


DATABASE_ENGINE = 'sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        }
}

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_flake8',
    'django_jenkins.tasks.run_jshint',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_sloccount',
    'django_jenkins.tasks.with_local_celery',
)


JSHINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/js/test.js')]
CSSLINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/css/test.css')]


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
