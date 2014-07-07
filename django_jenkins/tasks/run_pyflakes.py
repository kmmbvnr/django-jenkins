# -*- coding: utf-8 -*-
import os
import re
import sys
from pyflakes.scripts import pyflakes

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Reporter(object):
    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'pyflakes.report'), 'w')

        # run pyflakes tool with captured output
        old_stdout, pyflakes_output = sys.stdout, StringIO()
        sys.stdout = pyflakes_output
        try:
            for location in apps_locations:
                if os.path.isdir(location):
                    for dirpath, dirnames, filenames in os.walk(os.path.relpath(location)):
                        if dirpath.endswith(os.sep + 'south_migrations'):
                            continue

                        for filename in filenames:
                            if filename.endswith('.py'):
                                pyflakes.checkPath(os.path.join(dirpath, filename))
                else:
                    pyflakes.checkPath(os.path.relpath(location))
        finally:
            sys.stdout = old_stdout

        # save report
        pyflakes_output.seek(0)

        while True:
            line = pyflakes_output.readline()
            if not line:
                break
            message = re.sub(r': ', r': [E] PYFLAKES:', line)
            output.write(message)

        output.close()
