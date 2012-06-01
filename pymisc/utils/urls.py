try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

def get_url_builder(domain):
    """
    Returns url builder function, which can build url with concreate domain

    >>> url_builder = get_url_builder("http://localhost/")
    >>> url_builder("index.html")
    'http://localhost/index.html'
    >>> url_builder("/index.html")
    'http://localhost/index.html'
    >>> url_builder("some/action/", id=10, value=20)
    'http://localhost/some/action/?id=10&value=20'
    >>> url_builder2 = get_url_builder("http://localhost")
    >>> url_builder2("index.html")
    'http://localhost/index.html'
    """
    def url_builder(url, **kwargs):
        args = '?' + '&'.join([key+'='+str(value) for key, value in kwargs.items()])
        return urljoin(domain, url) + (args if kwargs else '')

    return url_builder

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
