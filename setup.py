#!/usr/bin/env python

import os.path as op
from distutils.core import setup

from zxcv import __version__, __author__


def read(fn):
    return open(op.join(op.dirname(__file__), fn), 'r').read()


setup(
    name='zxcv',
    version=__version__,
    author=__author__[:14],
    author_email=__author__[16:-1],
    license='BSD License',
    long_description=read('README'),
    packages=['zxcv', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries',
    ],
)
