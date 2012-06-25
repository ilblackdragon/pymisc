
class ReprToStr(object):
    """
    >>> class Example(ReprToStr):
            def __str__(self):
                return "example"
    >>> e = Example()
    >>> e
    "example"
    >>> print(e)
    "example"
    """
    
    def __repr__(self):
        return str(self)

def print_func(message):
    """
    >>> print_func("test message")
    test message
    """
    print(message)

def error_message(response, log_func=print_func):
    """
    Reports error based on response dictionary
    Searches for 'message' and 'exception' values

    >>> error_message({'message': "some message"})
    Message: some message
    >>> error_message({'exception': Exception("message")})
    Exception: message
    """
    if 'message' in response:
        log_func("Message: %s" % response['message'])
    if 'exception' in response:
        log_func("Exception: %s" % response['exception'])

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
