# -*- coding: utf-8 -*-

from errors import *
import requests
import unittest

class TestAPI(unittest.TestCase):

    def setUp(self):
        #self.url = 'http://wikette.freaxmind.pro/api.php'
        self.url = 'http://172.24.141.120/api.php'
        self.title = u"Valentin"
        self.unknown_title = u"Valise"
        self.content = u"<p><b>Valentin</b> est un <i>prénom</i> pour les grands romantiques."
        content = requests.publish(self.url, self.title, self.content)

    def test_invalid_host(self):
        self.assertRaisesRegexp(APIException, "Name or service not known", requests.get_article_content, "http://no.freaxmind.pro/api.php", "Valentin")

    def test_invalid_url(self):
        self.assertRaisesRegexp(APIException, "Not Found", requests.get_article_content, "http://wikette.freaxmind.pro/noapi.php", "Valentin")

    def test_unknown_title_exception(self):
        self.assertRaisesRegexp(APIException, "missingtitle", requests.get_article_content,self.url, self.unknown_title)

    def test_get_article_content(self):
        content = requests.get_article_content(self.url, self.title)
        self.assertTrue(u"<p><b>Valentin</b> est un <i>prénom</i> pour les grands romantiques." in content)

    def test_get_article_timestamp(self):
        from datetime import datetime

        # use publish to change the content time
        content = requests.publish(self.url, self.title, self.content+"aa")
        timestamp = requests.get_article_timestamp(self.url, self.title)
        content = requests.publish(self.url, self.title, self.content)
        self.assertEquals(timestamp.year, 2014)
        self.assertEquals(timestamp.hour, datetime.now().hour)

    def test_get_article_url(self):
        url = requests.get_article_url(self.url, self.title)
        self.assertTrue(self.title in url)
        url = requests.get_article_url(self.url, self.unknown_title)
        self.assertEquals(url, None)

    def test_search(self):
        # success
        result = requests.search(self.url, self.title)
        self.assertTrue(len(result) >= 2)
        self.assertTrue('url' in result[0].keys())
        self.assertTrue('description' in result[0].keys())
        self.assertTrue('title' in result[0].keys())
        self.assertTrue(self.title in result[0]['title'])
        # no result
        noresult = requests.search(self.url, self.unknown_title)
        self.assertTrue(len(noresult) == 0)

    def test_get_token(self):
        from lib import APIRequest

        request = APIRequest(self.url)
        edit_token = request.getToken(self.title, 'edit', True, True)
        self.assertTrue(len(edit_token) > 24)

    def test_publish(self):
        # update without change
        result = requests.publish(self.url, self.title, self.content)
        self.assertEquals(result, 0)
        # update with change
        result = requests.publish(self.url, self.title, self.content + "a")
        self.assertEquals(result, 1)
        # reset
        result = requests.publish(self.url, self.title, self.content)
        self.assertEquals(result, 1)
        # create
        from time import time
        title = 'www-' + str(time())
        #result = requests.publish(self.url, title, 'A'*24)
        #self.assertEquals(result, 2)
        print "DISABLE test_create"

    def test_conflict(self):
        from datetime import datetime

        last_timestamp = datetime(2014, 1, 9, 2, 40, 0)
        result = requests.publish(self.url, self.title, self.content, last_timestamp)
        self.assertEquals(result, -2)


if __name__ == '__main__':
    unittest.main()
