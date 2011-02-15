import sys

DEBUG=True
TEMPLATE_DEBUG=DEBUG
ROOT_URLCONF = 'test_app.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)


PROJECT_APPS = (
    'django.contrib.sessions', # just to enshure that dotted apps test works
    'django_jenkins',
    'test_app',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
) + PROJECT_APPS

DATABASE_ENGINE = 'sqlite3'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

# python > 2.4
if sys.version_info[1] > 4:
    JENKINS_TASKS += ('django_jenkins.tasks.run_pylint',
                      'django_jenkins.tasks.windmill_tests')
