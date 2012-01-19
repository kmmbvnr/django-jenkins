# -*- coding: utf-8; mode: django -*-
import os
import shelve
from django.conf import settings


class Storage(object):
    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def ci_root():
        ci_root = getattr(settings, 'CI_ROOT', os.path.join(settings.MEDIA_ROOT, 'ci'))
        if not os.path.exists(ci_root):
            os.makedirs(ci_root)
        return ci_root

    @staticmethod
    def open():
        storage = shelve.open(os.path.join(Storage.ci_root(), 'cidata.shelve'))
        if 'version' not in storage:
            storage['version'] = '1.0'
            if 'last_build_id' not in storage:
                storage['last_build_id'] = 0
        return Storage(storage=storage)

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __contains__(self, item):
        return item in self.storage

    def close(self):
        self.storage.close()

