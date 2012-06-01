import urllib
import urllib2
import json
from os.path import join

class Browser(object):

    def __init__(self, opener=None):
        if opener:
            self.opener = opener
        else:
            self.opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor()
            )
            self.opener.addheaders = [
                ('User-agent', 
                    ('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322')
                )
            ]

    def _get(self, url):
        response = self.opener.open(url)
        content = response.read()
        return content

    def _post(self, url, post_data):
        form_data = urllib.urlencode(post_data)
        response = self.opener.open(url, form_data)
        content = response.read()
        response.close()
        return content

    def get_json(self, url):
        try:
            response = self._get(url)
            return json.loads(response)
        except urllib2.URLError as e:
            return {
                'status': 'failed',
                'exception': e,
            }

    def post_json(self, url, post_data):
        try:
            response = self._post(url, post_data)
            return json.loads(response)
        except urllib2.URLError as e:
            return {
                'status': 'failed',
                'exception': e,
            }

    def download(self, url, dir, filename=None, file_opener=open):
        response = self._get(url)
        filename = filename if filename else url.split('/')[-1]
        f = file_opener(join(dir, filename), 'wb')
        f.write(response)
        f.close()
