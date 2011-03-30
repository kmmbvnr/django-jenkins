# -*- coding: utf-8 -*-
import subprocess

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
