# -*- coding: utf-8 -*-
import os.path
import subprocess

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
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]

        exception = subprocess.CalledProcessError(retcode, cmd)
        exception.output = output
        raise exception
    return output
