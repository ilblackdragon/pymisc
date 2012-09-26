"""
Simple Data Structures: 
Dict, DefaultDict, RecursiveDict, Struct, isiterable, make_iterable
"""

import copy

def isiterable(obj):
    return isinstance(obj, collections.Iterable)

def make_iterable(l1, l2):
    return l1 if isiterable(l1) else [l1], \
        l2 if isiterable(l2) else [l2]
    
def Dict(**entries):  
    """Create a dict out of the argument=value arguments. 
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

class DefaultDict(dict):
    """Dictionary with a default value for unknown keys.
    >>> d = DefaultDict([])
    >>> d[1].append(2)
    >>> d
    {1: [2]}
    """

    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        """
        >>> d = DefaultDict(0)
        >>> d[1] += 1
        >>> d[1]
        1
        """
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
    
    def __copy__(self):
        """
        >>> d = DefaultDict(0)
        >>> d[1] += 1
        >>> p = d.copy()
        >>> p
        {1: 1}
        """
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy
    
class RecursiveDict(dict):
    """Dictionary witch contains dictionary and that continues n-times, plust has a default value for unknown keys at last dictionary.
    >>> d = RecursiveDict(2, [])
    >>> d[1]['keyword'].append(5)
    >>> d[1]['keyword']
    [5]
    """

    def __init__(self, ncount, default = None):
        self.ncount = ncount - 1
        self.default = default

    def __getitem__(self, key):
        """
        >>> d = RecursiveDict(2, [])
        >>> d[1]['keyword'].append(5)
        >>> d[1]['keyword']
        [5]
        """
        if key in self: 
           return self.get(key)
        if self.ncount > 0:
           return self.setdefault(key, RecursiveDict(self.ncount - 1, self.default))
        return self.setdefault(key, copy.deepcopy(self.default))
    
    def __copy__(self):
        """
        >>> d = RecursiveDict(2, [])
        >>> d[1]['keyword'].append(5)
        >>> p = d.copy()
        >>> p
        {1: {'keyword': [5]}}
        """
        copy = RecursiveDict(self.ncount, self.default)
        copy.update(self)
        return copy
    
class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter.
    >>> a = Struct(a=1, b=2, c=3)
    >>> a.a
    1
    >>> a.b
    2
    >>> a.c
    3
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        """
        >>> a = Struct(a=1, b=2, c=3)
        >>> b = Struct(a=1, b=2, c=3)
        >>> c = Struct(a=3, b=2, c=3)
        >>> a == b
        True
        >>> a == c
        False
        """
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
