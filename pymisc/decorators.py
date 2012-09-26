"""
Module contains different decorator for different purpose
"""
import sys
import logging
import functools

class LogPrinter(object):
    """
    LogPrinter class which serves to emulates a file object and logs
    whatever it gets sent to a Logger object at the INFO level
    """
    
    def __init__(self, logger=None):
        """Grabs the specfic logger to use for logprinting."""
        if not logger:
            self.ilogger = logging.getLogger('logprinter')
            il = self.ilogger
            logging.basicConfig()
            il.setLevel(logging.INFO)
        else:
            self.ilogger = logger

    def write(self, text):
        """Logs written output to a specific logger"""
        if text.strip() != '':
            self.ilogger.info(text)

def logprint(logger=None):
    """Wraps a method so that any calls made to print get logger instead"""

    def wrapped_func(func):
        @functools.wraps(func)
        def wrapped_f(*args, **kwargs):
            stdobak = sys.stdout
            lpinstance = LogPrinter(logger)
            sys.stdout = lpinstance
            lpinstance.write('Call `%s.%s` with args: `%s` and kwargs: `%s`' % (func.__module__, func.__name__, str(args), str(kwargs)))
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                lpinstance.write('Function `%s.%s` finished with exception `%s`.\n%s' % (func.__module__, func.__name__, str(type(e)), str(e)))
                raise e
            else:
                lpinstance.write('Function `%s.%s` finished with result `%s`.' % (func.__module__, func.__name__, str(res)))
            finally:
                sys.stdout = stdobak
            return res
        return wrapped_f
    return wrapped_func
   
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
 
