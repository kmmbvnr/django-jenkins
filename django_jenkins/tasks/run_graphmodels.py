# -*- coding: utf-8 -*-
# pylint: disable=W0201
import os
from optparse import make_option
from django.conf import settings
from django.core.management import call_command, CommandError
from django_jenkins.tasks import BaseTask, get_apps_under_test


class Task(BaseTask):
    # Using options from modelviz.py / graph_models.py, prefixed with
    # graphmodels[_-]
    option_list = [
        make_option('--graphmodels-disable-fields',
                    action='store_true', dest='graphmodels_disable_fields',
            help='Do not show the class member fields'),
        make_option('--graphmodels-group-models',
                    action='store_true', dest='graphmodels_group_models',
            help='Group models together respective to their application'),
        make_option('--graphmodels-all-applications',
                    action='store_true', dest='graphmodels_all_applications',
            help='Automatically include all applications from INSTALLED_APPS'),
        make_option('--graphmodels-output',
                    action='store', dest='graphmodels_outputfile',
            help='Render output file. Type of output dependend on file'
                     ' extensions. Use png or jpg to render graph to image.'),
        make_option('--graphmodels-layout',
                    action='store', dest='graphmodels_layout', default='dot',
            help='Layout to be used by GraphViz for visualization. Layouts: '
                 'circo dot fdp neato nop nop1 nop2 twopi'),
        make_option('--graphmodels-verbose-names',
                    action='store_true', dest='graphmodels_verbose_names',
            help='Use verbose_name of models and fields'),
        make_option('--graphmodels-language',
                    action='store', dest='graphmodels_language',
            help='Specify language used for verbose_name localization'),
        make_option('--graphmodels-exclude-columns',
                    action='store', dest='graphmodels_exclude_columns',
            help='Exclude specific column(s) from the graph. Can also load '
                 'exclude list from file.'),
        make_option('--graphmodels-exclude-models',
                    action='store', dest='graphmodels_exclude_models',
            help='Exclude specific model(s) from the graph. Can also load '
                 'exclude list from file.'),
        make_option('--graphmodels-inheritance',
                    action='store_true', dest='graphmodels_inheritance',
            help='Include inheritance arrows'),
    ]

    def checkdeps(self):
        if 'django_extensions' not in settings.INSTALLED_APPS:
            if self.options.get('fail_without_error', False):
                return False
            else:
                raise CommandError("django-extensions is required to execute"
                                   " this command")

        try:
            import pygraphviz  # noqa
        except ImportError:
            if self.options.get('fail_without_error', False):
                return False
            else:
                raise CommandError("pygraphviz is required to execute "
                                   "this command")

        return True

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.options = options

        # Rename options, for the call to the existing graph_models command
        for key, value in self.options.items():
            if key.startswith('graphmodels_'):
                newkey = key[12:]
                del self.options[key]
                self.options[newkey] = value

        # Merge in possibles settings file options, if the option is
        # unset (None)
        fromfile = getattr(settings, 'GRAPH_MODELS', {})
        fromfile.update(dict((k, v) for k, v in self.options.iteritems() if v))
        self.options.update(fromfile)

        if self.options['test_all']:
            self.options['all_applications'] = True

        # Place the file in the correct place
        output_dir = self.options['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.options['outputfile'] = os.path.join(output_dir, 'models.png')

        if not self.checkdeps():
            return

    def teardown_test_environment(self, **kwargs):
        # Get the list of PROJECT_APPS if nothing specified any we don't
        # want everything
        if len(self.test_labels) < 1 and not self.options['all_applications']:
            under = get_apps_under_test(self.test_labels,
                                        self.options['all_applications'])
            self.test_labels = [label.split('.')[-1] for label in under]

        call_command('graph_models', *self.test_labels, **self.options)
