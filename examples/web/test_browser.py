import json
import urllib
import urllib2
from mock import Mock
import unittest
from os.path import join

from pymisc.web.browser import Browser

TEST_URL = 'http://localhost/'
TEST_SOME_DATA = {"some": "data", "qq": 1, "bla": [1, 2]}
TEST_POST_DATA = {'some': 'data'}
TEST_SOME_FILE_CONTENT = "adasdasdasdksa;dsld;salkf;lgkf;lks;dlkasdasd"
TEST_LOCAL_DIR = "/local/dir"
TEST_FILENAME = "somefile.dat"

class TestBrowser(unittest.TestCase):
    
    def setUp(self):
        self.writer = Mock()
        self.writer.write = Mock()
        self.file_opener = Mock(return_value=self.writer)
        self.response = Mock()
        self.url_opener = Mock()

        self.browser = Browser(self.url_opener)
        
    def test_get_json(self):
        self.response.read = Mock(return_value=json.dumps(TEST_SOME_DATA))
        self.url_opener.open = Mock(return_value=self.response)
        result = self.browser.get_json(TEST_URL)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, TEST_SOME_DATA)
        self.url_opener.open.assert_called_with(TEST_URL)

    def test_get_json_exception(self):
        self.url_opener.open = Mock(side_effect=urllib2.HTTPError(TEST_URL, 500, "Server is down", None, None))
        result = self.browser.get_json(TEST_URL)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('exception', result)
        self.url_opener.open.assert_called_with(TEST_URL)
        
    def test_post_json(self):
        self.response.read = Mock(return_value=json.dumps(TEST_SOME_DATA))
        self.url_opener.open = Mock(return_value=self.response)
        result = self.browser.post_json(TEST_URL, TEST_POST_DATA)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, TEST_SOME_DATA)
        self.url_opener.open.assert_called_with(TEST_URL, urllib.urlencode(TEST_POST_DATA))

    def test_post_json_exception(self):
        self.url_opener.open = Mock(side_effect=urllib2.HTTPError(TEST_URL, 500, "Server is down", None, None))
        result = self.browser.post_json(TEST_URL, TEST_POST_DATA)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('exception', result)
        self.url_opener.open.assert_called_with(TEST_URL, urllib.urlencode(TEST_POST_DATA))
        
    def test_download_file(self):
        self.response.read = Mock(return_value=TEST_SOME_FILE_CONTENT)
        self.url_opener.open = Mock(return_value=self.response)
        self.browser.download(TEST_URL, TEST_LOCAL_DIR, TEST_FILENAME, file_opener=self.file_opener)
        
        self.url_opener.open.assert_called_with(TEST_URL)
        self.file_opener.assert_called_with(join(TEST_LOCAL_DIR, TEST_FILENAME), 'wb')
        self.writer.write.assert_called_with(TEST_SOME_FILE_CONTENT)
