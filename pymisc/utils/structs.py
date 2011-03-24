"""
Simple Data Structures: 
Dict, DefaultDict, RecursiveDict, Struct
"""

import copy as cccopy

def Dict(**entries):  
    """Create a dict out of the argument=value arguments. 
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""

    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, cccopy.deepcopy(self.default))
    
    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy
    
class RecursiveDict(dict):
    """Dictionary witch contains dictionary and that continues n-times, plust has a default value for unknown keys at last dictionary."""

    def __init__(self, ncount, default = None):
        self.ncount = ncount - 1
        self.default = default

    def __getitem__(self, key):
        if key in self: 
           return self.get(key)
        if self.ncount > 0:
           return self.setdefault(key, RecursiveDict(self.ncount - 1, self.default))
        return self.setdefault(key, copy.deepcopy(self.default))
    
    def __copy__(self):
        copy = RecursiveDict(self.ncount, self.default)
        copy.update(self)
        return copy
    
class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)   
    else:
        x.__dict__.update(entries) 
    return x 
