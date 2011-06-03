"""
Settings class
Yours settings.py:
>>> from pymisc.settings import Settings
>>> settings = Settings('your.cfg')
>>> settings.default('MYVAR', 10)
Your code file:
>>> from settings import settings
...
>>> if settings.MYVAR > 10:
>>>    pass
...
"""

import os.path
import atexit
from config import Config

class Settings(Config):
    
    def __init__(self, filename, autosave=True):
        object.__setattr__(self, 'filename', filename)
        loaded = False
        if filename != None and os.path.exists(filename):
            try:
                f = open(filename)
                super(Settings, self).__init__(f)
                loaded = True
            except Exception as e:
                print("Loading configuration file failed with error:\n`%s`" % e)
        if not loaded:
            super(Settings, self).__init__()
        if autosave:
            atexit.register(getattr(self, 'save'))

    def save(self, filename=None):
        fname = filename or object.__getattribute__(self, 'filename')
        if not fname:
            return
        Config.save(self, open(fname, 'wb'))

    def default(self, key, value):
        try:
            getattr(self, key)
        except AttributeError:
            self.__setattr__(key, value)


