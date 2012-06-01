from datetime import datetime, timedelta

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def date2str(date):
    """
    Converts date to string, with specific format

    >>> date2str(datetime(2012, 1, 1, 2, 3, 4))
    '2012-01-01 02:03:04'
    >>> now = datetime.now()
    >>> str2date(date2str(now)) - now < timedelta(seconds=1)
    True
    """
    return datetime.strftime(date, DATETIME_FORMAT)
    
def str2date(str):
    """
    Converts string to date, with specific format
    
    >>> str2date('2012-01-01 02:03:04')
    datetime.datetime(2012, 1, 1, 2, 3, 4)
    """
    return datetime.strptime(str, DATETIME_FORMAT)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
