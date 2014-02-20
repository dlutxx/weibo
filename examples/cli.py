#-*- coding: utf8 -*-
from __future__ import print_function

import weibo


class App(object):
    ''' Terminal weibo client'''

    def __init__(self, ak=None):
        pass


class Config(object):

    def __init__(self, opts=None, **kwargs):
        self.__dict__['_opts'] = opts or dict()
        self._opts.update(kwargs)

    def __getattr__(self, key):
        return self._opts.get(key, None)

    def __setattr__(self, key, val):
        self._opts[key] = val

    @classmethod
    def loadfile(cls, filepath):
        with open(filepath) as fin:
            return cls.loadstr(fin.read())

    @classmethod
    def loadstr(cls, optstr):
        opts = {}
        for line in optstr.split('\n'):
            line = line.strip()
            if (line.startswith('#')  # comment
               or line.startswith('[')):  # block tag
                continue
            parts = line.split('=', 1)
            if len(parts) > 1:
                opts[parts[0].strip()] = parts[1].strip()
        return cls(opts)


def main():
    App().mainloop()


if __name__ == '__main__':
    main()
