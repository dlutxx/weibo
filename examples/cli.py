#-*- coding: utf8 -*-
from __future__ import print_function

import weibo
import curses
import logging


class Command(object):
    pass

class App(object):
    ''' Terminal weibo client'''

    def __init__(self, cfg):
        self.cfg = cfg
        self.weibo = weibo.Client(cfg.access_key)

    def dispatch(self, ch):
        cmd = self.map_key(ch)
        if cmd:
            try:
                self.run_cmd(cmd, ch)
            except Exception as e:
                pass

    def map_key(self, ch):
        pass

    def run_cmd(self, cmd, ch):
        pass

    def mainloop(self, stdscr):
        self.scr = stdscr
        while True:
            ch = stdscr.getch()
            self.dispatch(ch)


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
    app = App(Config.loadfile('~/.weiborc'))
    curses.wrapper(app.mainloop)


if __name__ == '__main__':
    main()
