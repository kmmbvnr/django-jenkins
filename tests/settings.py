import os, sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG=True
TEMPLATE_DEBUG=DEBUG
ROOT_URLCONF = 'test_app.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)

PROJECT_APPS = (
    'django.contrib.sessions', # just to ensure that dotted apps test works
    'django_jenkins',
    'test_app',
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
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_jslint',
    'django_jenkins.tasks.run_csslint',    
    'django_jenkins.tasks.run_sloccount',    
    'django_jenkins.tasks.lettuce_tests',
)

JSLINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/js/test.js')]
CSSLINT_CHECKED_FILES = [os.path.join(PROJECT_ROOT, 'static/css/test.css')]

# python > 2.4
if sys.version_info[1] > 4:
    JENKINS_TASKS += ('django_jenkins.tasks.run_pylint',)
