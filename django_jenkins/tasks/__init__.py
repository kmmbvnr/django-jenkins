import os
import itertools

from django.conf import settings
from django.contrib.staticfiles import finders


def static_files_iterator(tested_locations, extension, ignore_patterns=None, additional_settings_list=None):
    if ignore_patterns is None:
        ignore_patterns = []

    source = (os.path.join(storage.location, path)
              for finder in finders.get_finders()
              for path, storage in finder.list(ignore_patterns))

    if additional_settings_list and hasattr(settings, additional_settings_list):
        source = itertools.chain(source, getattr(settings, additional_settings_list))

    return (path for path in source
            if path.endswith(extension)
            if any(path.startswith(location) for location in tested_locations))


def set_option(conf_dict, opt_name, opt_value, conf_file, default=None, split=None):
    if conf_file is None:
        if opt_value is None:
            opt_value = default

    if opt_value:
        if split:
            opt_value = opt_value.split(split)

        conf_dict[opt_name] = opt_value
