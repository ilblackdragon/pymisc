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

FULL_URL_EXTRACTOR_RE = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
HREF_URL_EXTRACTOR_RE = re.compile(r'href=[\'"]?([^\'" >]+)')

def url_localify(url, origin_url):
    """
    Ensure that input url will be full and if it's not add domain from origin_url

    >>> url_localify('/about/', 'http://qq.com/terms/')
    http://qq.com/about
    >>> url_localify('terms/', 'http://qq.com/about')
    http://qq.com/about/terms/about
    >>> url_localify('http://test.com/about', 'http://qq.com/about')
    http://test.com/about
    """
    return urljoin(origin_url, url)

def extract_urls(content, origin_url=None, url_re=HREF_URL_EXTRACTOR_RE, url_re_group=1):
    """
    Extract list of urls from content.
    If origin_url passed - localify urls to make local urls /foobar/ with domain

    url_re and url_re_group - ensures extensibility of this funciton

    >>> [x for x in extract_url("asdasd <a href="/stuff">stuff</a> <a href="http://google.com/">google</a>", "http://qq.com/")]
    ["http://qq.com/stuff/", "http://google.com/"]
    """
    for match in url_re.finditer(content):
        url = match.group(url_re_group)
        if origin_url:
            url = url_localify(url, origin_url)
        yield url


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

