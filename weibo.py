#-*- encoding: utf-8 -*-
'''支持Python 2、3的微博客户端类

微博的接口文档： http://open.weibo.com/wiki/%E9%A6%96%E9%A1%B5

Example Usage:

    # 登陆页,将用户浏览器重定向到 auth.auth_url() 进行授权
    >>> auth = OAuth(client_id=my_client_id, redirect_uri=myredirect_uri)
    >>> print(auth.auth_url(state="my_token", display="mobile"))
    https://api.weibo.com/oauth2/authorize?client_id=123050457758183&redirect_uri=http://www.example.com/response&response_type=code

    # 微博授权回调页面，用code换取access_token
    >>> code = request.GET['code']
    >>> auth = OAuth(client_id=my_client_id, client_sec=code,
                 redirect_uri=redirect_uri)
    >>> print(auth.access_token(code))
    {"access_token": "ACCESS_TOKEN", "expires_in": 1234, "remind_in":"798114", "uid":"12341234"}
    
    # 有了access_token，就可以实例化Client来操作微博了
    >>> client = Client(my_access_token)
    >>> client.update('test weibo')
    {"created_at": "...", "id": "123",...}
'''

__all__ = ['OAuth', 'Client']
__version__ = (0, 1, 0)
__author__ = 'dlutxx@gmail.com'


import json
try:  # Python 3
    from urllib.request import urlopen, Request as _Request
    from urllib.parse import urlencode, quote_plus

    def Request(url, data=None, *args, **kwargs):
        if data:
            data = data.encode(DEFAULT_CHARSET)
        return _Request(url, data, *args, **kwargs)
except ImportError:  # Python 2
    from urllib2 import urlopen, Request
    from urllib import urlencode, quote_plus


# default charset for http requests and reponses
DEFAULT_CHARSET = 'utf8'


def q(url, data=None, headers=None, force_get=False):
    ''' 发起get/post http请求，并返回json decoded数据

    data: 请求的参数，None或者mapping类型
    headers: http请求头, None或者mapping类型
    force_get: 是否强制使用GET方式
    '''
    if data:
        data = urlencode(data)
    if force_get:
        if url.find('?') > -1:
            url = '%s&%s' % (url, data)
        else:
            url = '%s?%s' % (url, data)
        request = Request(url, None, headers or {})
    else:
        request = Request(url, data, headers or {})
    response = urlopen(request)
    if response.msg != 'OK':
        raise HttpError(response)
    return json.loads(response.read().decode(DEFAULT_CHARSET))


class HttpError(Exception):
    pass


class OAuth(object):
    ''' 微博授权辅助类

    微博授权机制说明:
    http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E
    '''
    api = 'https://api.weibo.com/oauth2/'
    def __init__(self, client_id='', redirect_uri='', client_sec=''):
        '''client_sec 只在用code换取access_token时才需要'''
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.client_sec = client_sec

    def auth_url(self, **opts):
        '''返回让用户授权的链接

        opts可指定额外传给授权页的参数，详见微博文档:
        http://open.weibo.com/wiki/Oauth2/authorize
        '''
        data = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        args = urlencode(data)
        return OAuth.api + 'authorize' + '?' + args

    def access_token(self, code):
        ''' 返回用code获取到access_token信息(dict)
        如果获取access_token失败，返回的dict包含失败详情

        code是微博传过来的参数,详见微博文档:
        http://open.weibo.com/wiki/Oauth2/access_token
        '''
        data = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'client_secret': self.client_sec,
            'grant_type': 'authorization_code',
            'code': code,
        }
        return q(OAuth.api + 'access_token', data)


class Client(object):
    '''操作微博API的客户端

    你可以通过home_line, update等对应于微博api的方法操作api，
    也可以通过get/post方法,将api名称当做参数传入,来直接访问api.
    '''
    def __init__(self, access_token):
        self.token = access_token
        self.uri = 'https://api.weibo.com/2/'

    def get(self, api, **data):
        ''' 通过GET方式访问api

        如果有api参数通过kwargs指定
        '''
        data.setdefault('access_token', self.token)
        return q(self.uri + api + '.json', data=data, force_get=True)

    def post(self, api, **data):
        ''' 通过POST方式访问api

        如果有api参数通过kwargs指定
        '''
        data.setdefault('access_token', self.token)
        return q(self.uri + api + '.json', data)

    def home_line(self, **opts):
        return self.get('statuses/friends_timeline', **opts)

    def update(self, status):
        return self.post('statuses/update', status=status)
