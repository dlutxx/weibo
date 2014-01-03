weibo
=====

精简的微博Python SDK, 兼容Python 2.7+ 和 3k，不依赖标准库之外的任何lib。
更重要的是，有单元测试哦！

Lean weibo client sdk for python 2 and 3, No dependency on any libs other than standard python lib.
What's more, it is unittested!.

    # 登陆页,将用户浏览器重定向到 auth.auth_url() 进行授权
    >>> auth = OAuth(client_id=my_client_id, redirect_uri=myredirect_uri)
    >>> print(auth.auth_url(state="my_token", display="mobile"))
    https://api.weibo.com/oauth2/authorize?client_id=123050457758183
    &redirect_uri=http://www.example.com/response&response_type=code

    # 微博授权回调页面，用code换取access_token
    >>> code = request.GET['code']
    >>> auth = OAuth(client_id=my_client_id, client_sec=code,
                 redirect_uri=redirect_uri)
    >>> print(auth.access_token(code))
    {"access_token": "ACCESS_TOKEN", "expires_in": 1234, "remind_in":
    "798114", "uid":"12341234"}

    # 有了access_token，就可以实例化Client来操作微博了
    >>> client = Client(my_access_token)
    >>> client.update('test weibo')
    {"created_at": "...", "id": "123",...}

[Documentation](https://github.com/dlutxx/weibo/blob/master/weibo.py)
