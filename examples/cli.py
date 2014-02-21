#-*- coding: utf8 -*-
from __future__ import print_function

import os.path
import sys
import weibo
import curses
import logging


if sys.version_info > (3,): # Python 3
    exec('''
def exec_in(code, glob, loc=None):
    if isinstance(code, str):
        code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, glob, loc)
''')
    exec_in('''
def with_meta(cls):
    class Base(metaclass=cls):
        pass
    return Base
    ''', globals())
else:
    exec('''
def exec_in(code, glob, loc=None):
    if isinstance(code, str):
        code = compile(code, '', 'exec', dont_inherit=True)
    exec code in glob, loc
''')
    exec_in('''
def with_meta(cls):
    class Base(object):
        __metaclass__ = cls
        pass
    return Base
''', globals())


def _init_logger(filename='cli.log', level=logging.DEBUG):
    logger = logging.getLogger('cliweibo')
    logger.setLevel(level)
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = _init_logger()

class _CommandRegistry(object):

    def __init__(self):
        self._classes = {}
        self._instances = {}
        self.default_keymap = {}
        self.app = None

    def find(self, name):
        name = name.lower()
        inst = self._instances.get(name, None)
        if inst is None:
            kls = self._classes.get(name, None)
            if kls is not None:
                inst = kls(self.app)
                self._instances[name] = inst
        return inst

    def register_class(self, name, cmd_class):
        self._classes[name] = cmd_class
        self.default_keymap[cmd_class.default_key] = name


cmds = _CommandRegistry()


class CommandMeta(type):

    @classmethod
    def is_real_command(kls, name):
        return not name in ('Base', 'Command')

    def __new__(kls, name, bases, attrs):
        if kls.is_real_command(name):
            attrs.setdefault('name', name.lower())
        return super(CommandMeta, kls).__new__(kls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        if CommandMeta.is_real_command(name):
            cmds.register_class(name.lower(), self)


class Command(with_meta(CommandMeta)):

    name = None
    description = None
    default_key = None

    def __init__(self, app):
        self.app = app

    def __call__(self):
        raise NotImplementedError


class Homeline(Command):
    ''' get home_timeline statuses '''

    default_key = 'h'

    def __call__(self):
        pass


class Update(Command):
    '''status updating command'''

    default_key = 'u'


class Quit(Command):
    ''' quit the app '''

    default_key = 'q'

    def __call__(self):
        self.app.stop()


class App(object):
    ''' Terminal weibo client'''
    instance = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.weibo = weibo.Client(cfg.access_key)
        cmds.app = self
        self._stopped = False

    def dispatch(self, ch):
        logger.debug('dispatch %d' % ch)
        cmd = self.map_key(ch)
        if cmd:
            try:
                self.run_cmd(cmd, ch)
            except Exception as e:
                logger.debug(e)

    def map_key(self, ch):
        ch = chr(ch)
        cmd_name = self.cfg['key.%s' % ch]
        if not cmd_name:
            cmd_name = cmds.default_keymap.get(ch, None)
        if cmd_name:
            return cmds.find(cmd_name)

    def run_cmd(self, cmd, ch):
        cmd()

    def stop(self):
        self._stopped = True

    def mainloop(self, stdscr):
        self.scr = stdscr
        while not self._stopped:
            ch = stdscr.getch()
            self.dispatch(ch)


class Config(object):

    COMMENT_MARK = '#'
    SECTION_START_MARK = '['
    SECTION_END_MARK = ']'

    def __init__(self, opts=None, **kwargs):
        self.__dict__['_opts'] = opts or dict()
        self._opts.update(kwargs)

    def __getitem__(self, key):
        return self._opts.get(key, None)

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
        section = ''
        for line in optstr.split('\n'):
            line = line.strip()
            if line.startswith(cls.COMMENT_MARK):
                continue
            if (line.startswith(cls.SECTION_START_MARK)
                and line.endswith(cls.SECTION_END_MARK)):
                section = line[1:-1].strip()
                continue
            parts = line.split('=', 1)
            if len(parts) > 1:
                key, val = parts[0].strip(), parts[1].strip()
                if section:
                    key = '%s.%s' % (section, key)
                opts[key] = val
        return cls(opts)


def main(argv):
    cfgfile = os.path.expanduser('~/.weiborc')
    app = App(Config.loadfile(cfgfile))
    curses.wrapper(app.mainloop)


if __name__ == '__main__':
    main(sys.argv)