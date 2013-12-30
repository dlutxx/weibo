#-*- encoding: utf-8 -*-
from __future__ import print_function

import sys
import time
import unittest
import weibo


class _Config(object):
    def __init__(self, client_id, client_secret, redirect_uri,
                 access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token

    def configed(self):
        return (self.client_id is not None and
               self.client_secret is not None and
               self.redirect_uri is not None)

# 如果想测试SDK，请填写以下信息
# uid = 1780753881
conf = _Config(client_id='1604135305',
               client_secret='f073e62f45afd48596f5885f063ba814',
               redirect_uri='http://idjango.sinaapp.com/oauth/weibo/auth',
               access_token='2.00n7rVwBFsmYkB6fbbe79617L6uFMD'
)


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


@unittest.skipIf(not conf.configed(), '请更新配置信息以便测试授权类')
class OAuthTest(unittest.TestCase):
    def test_auth(self):
        auth = weibo.OAuth(conf.client_id, conf.redirect_uri,
                           conf.client_secret)
        url = auth.auth_url()
        self.assertTrue(url.startswith('http'))
        print("点击此链接授权: %s" % url)
        print("输入授权后url的code: ")
        code = sys.stdin.readline().strip()
        if code:
            ret = auth.access_token(code)
            err = '获取access_token失败: %s' % ret
            self.assertIn('access_token', ret, err)
            print(ret)


@unittest.skipIf(conf.access_token is None, '请填写access_token以测试')
class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = weibo.Client(conf.access_token)

    def test_home_timeline(self):
        line = self.client.home_timeline()
        self.assertIn('statuses', line, '获取home_timeline失败')

    def test_update_and_destroy(self):
        now = time.strftime('%Y%m%d %H:%M:%S')
        status = "Lean and Tested Weibo SDK for Python 2 and"\
            " 3: https://github.com/dlutxx/weibo , %s" % now
        post = self.client.update(status)
        self.assertIn('id', post)
        ret = self.client.destroy(post['id'])
        self.assertIn('id', ret)
        self.assertEqual(post['id'], ret['id'])


if __name__ == '__main__':
    unittest.main()
