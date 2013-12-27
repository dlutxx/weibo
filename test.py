#-*- encoding: utf-8 -*-
from __future__ import print_function

import unittest
import weibo


# 如果想测试SDK，请填写一下信息
CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = None
CODE = None
ACCESS_TOKEN = None


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


@unittest.skipIf(CLIENT_ID is None or
    CLIENT_SECRET is None or
    REDIRECT_URI is None, '请更新配置信息以便测试授权类')
class OAuthTest(unittest.TestCase):
    def setUp(self):
        self.auth = weibo.OAuth(KEY, URI, SEC)

    def test_auth_url(self):
        url = self.auth.auth_url()
        self.assertTrue(url.startswith('http'))

    def test_access_token(self):
        ret = self.auth.access_token(code)
        err = '获取access_token失败: %s' % ret
        self.assertIn('access_token', ret, err)


@unittest.skipIf(ACCESS_TOKEN is None, '请填写access_token以测试')
class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = weibo.Client(ACCESS_TOKEN)

    def test_home_line(self):
        line = self.client.home_line()
        self.assertIn('statuses', line)

    def test_update(self):
        post = self.client.update("Lean and Tested Python Weibo"
            " SDK from: https://github.com/dlutxx/weibo")
        self.assertIn('mid', post)


if __name__ == '__main__':
    unittest.main()
