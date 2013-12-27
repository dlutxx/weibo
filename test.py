#-*- encoding: utf-8 -*-
from __future__ import print_function

import unittest
import weibo


KEY = '1604135309'
SEC = 'f073e62f49afd48596f5885f063ba814'
URI = 'http://idjango.sinaapp.com/oauth/weibo/auth'
TOKEN = '2.00n7r9wBFsmYkB6fbbe79617L6uFMD'


class QTest(unittest.TestCase):
    def test_get(self):
        url = 'http://httpbin.org/get?name=abc'
        ret = weibo.q(url, headers={'X-Test': 'yes'})
        self.assertIn('args', ret)
        self.assertIn('name', ret['args'])
        self.assertIn('X-Test', ret['headers'])

    def test_post(self):
        url = 'http://httpbin.org/post'
        ret = weibo.q(url, {'name': 'abc'}, {'X-Test': 'yes'})
        self.assertIn('form', ret)
        self.assertIn('name', ret['form'])
        self.assertIn('X-Test', ret['headers'])


@unittest.skip
class OAuthTest(unittest.TestCase):
    def setUp(self):
        self.auth = weibo.OAuth(KEY, URI, SEC)

    def test_auth_url(self):
        print(self.auth.auth_url())

    def test_access_token(self):
        print(self.auth.access_token('15635c3bb1e7361bf8bf3f56107af884'))


@unittest.skip
class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = weibo.Client(TOKEN)

    def test_home_line(self):
        line = self.client.home_line()
        self.assertIn('statuses', line)

    def test_update(self):
        post = self.client.update("hahaha^_^")
        self.assertIn('mid', post)


if __name__ == '__main__':
    unittest.main()
