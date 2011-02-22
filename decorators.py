"""
Module contains different decorator for different purpose
"""
import logging

class LogPrinter(object):
    """
    LogPrinter class which serves to emulates a file object and logs
    whatever it gets sent to a Logger object at the INFO level
    """
    
    def __init__(self):
        """Grabs the specfic logger to use for logprinting."""
        self.ilogger = logging.getLogger('logprinter')
        il = self.ilogger
        logging.basicConfig()
        il.setLevel(logging.INFO)

    def write(self, text):
        """Logs written output to a specific logger"""
        self.ilogger.info(text)

def logprint(func):
    """Wraps a method so that any calls made to print get logger instead"""
    def pwrapper(*arg):
        stdobak = sys.stdout
        lpinstance = LogPrinter()
        sys.stdout = lpinstance
        try:
            return func(*arg)
        finally:
            sys.stdout = stdobak
    return pwrapper

class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """

   def __init__(self, func):
      self.func = func
      self.cache = {}

   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         value = self.func(*args)
         self.cache[args] = value
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args)
   
   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

