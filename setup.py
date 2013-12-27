# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='weibo',
    version='0.1.0',
    description='Lean Python SDK for Weibo',
    author='dlutxx',
    author_email='dlutxx@gmail.com',
    py_modules=['weibo', ],
    package_data={'': ['LICENSE'], },
    url='https://github.com/dlutxx/weibo',
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
)
