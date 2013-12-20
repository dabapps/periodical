#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    module = open('periodical.py').read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", module).group(1)


version = get_version()


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='periodical',
    version=version,
    url='https://github.com/dabapps/periodical',
    license='BSD',
    description='A library for working with time and date series.',
    author='Tom Christie',
    author_email='tom@tomchristie.com',
    py_modules=['periodical'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
