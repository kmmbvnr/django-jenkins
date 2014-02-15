# -*- coding: utf-8 -*-
import os.path
import subprocess


class CalledProcessError(subprocess.CalledProcessError):
    def __init__(self, returncode, cmd, output=None):
        super(CalledProcessError, self).__init__(returncode, cmd)
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d\nOutput:\n%s" \
            % (self.cmd, self.returncode, self.output)


def relpath(path, start=os.path.curdir):
    """
    Return a relative version of a path

    Backport from Python2.7
    """
    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [os.path.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return os.path.curdir
    return os.path.join(*rel_list)


def check_output(*popenargs, **kwargs):
    """
    Backport from Python2.7
    """
    if 'stdout' in kwargs or 'stderr' in kwargs:
        raise ValueError('stdout or stderr argument not allowed, '
                         'it will be overridden.')

    try:
        process = subprocess.Popen(stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   *popenargs, **kwargs)
    except OSError:
        raise RuntimeError('Could not open program %s. Are the dependencies installed?' % popenargs)

    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output="%s\n%s" % (output, err))
    return output


def find_first_existing_executable(exe_list):
    """
    Accepts list of [('executable_file_path', 'options')],
    Returns first working executable_file_path
    """
    for filepath, opts in exe_list:
        try:
            proc = subprocess.Popen([filepath, opts],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            proc.communicate()
        except OSError:
            pass
        else:
            return filepath


def total_seconds(delta):
    """
    Backport timedelta.total_seconds() from Python 2.7
    """
    return delta.days * 86400.0 + delta.seconds + delta.microseconds * 1e-6
