import os, sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG=True
TEMPLATE_DEBUG=DEBUG
ROOT_URLCONF = 'test_app.urls'
SITE_ID = 1

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader', 
    'django.template.loaders.app_directories.Loader', 
)

PROJECT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_jenkins',
    'test_app',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
) + PROJECT_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    }
}


JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_jslint',
)

JSLINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/js/test.js')]

# python > 2.4
if sys.version_info[1] > 4:
    JENKINS_TASKS += ('django_jenkins.tasks.run_pylint',
                      'django_jenkins.tasks.windmill_tests')
