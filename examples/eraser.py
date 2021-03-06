# -*- encoding: utf8 -*-
'''清空博主的所有微博'''


from __future__ import print_function
from weibo import Client


def erase(uid, access_key):
    client = Client(access_key)
    while True:
        ret = client.status.user_timeline(uid=uid, count=100)
        if not ret['statuses']:
            break
        for st in ret['statuses']:
            print("Deleting %s: %s" % (st['id'], st['text']))
            client.status.destroy(st['id'])


if __name__ == '__main__':
    erase(1625287522, '2.00sWXzlBk5pPEC34765094ba9uZ9CD')
