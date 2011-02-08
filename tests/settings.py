DEBUG=True
TEMPLATE_DEBUG=DEBUG
ROOT_URLCONF = 'test_app.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)


INSTALLED_APPS = (
    'django.contrib.sessions', # just to enshure that dotted apps test works
    'django_hudson',
    'test_app',)
DATABASE_ENGINE = 'sqlite3'
