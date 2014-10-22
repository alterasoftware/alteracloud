"""
Unapologetically adapted from Jeff Knupp's execellent article:

http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
"""
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import alteracloud

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = """The ``alteracloud`` python API allows you to login, query and 
use the various services provided by the Altera Cloud in its REST API.

The official documentation for the project can be found here: <?>

The source code for the project can be found here: <?>
"""

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name = 'alteracloud',
    version = alteracloud.__version__,
    url = 'https://cloud.altera.com/developer/',
    license = 'MIT',    
    author = 'Robert Romano',
    tests_require = ['tox'],
    install_requires = [
        'requests',
        'py>=1.4.20',    
        'tox>=1.7.1',
        'virtualenv>=1.11.4',
    ],
    cmdclass = {'test': Tox},
    author_email = 'rromano@altera.com',
    description = 'A Python interface to the Altera Cloud REST API',
    long_description = long_description,
    packages = ['alteracloud'],
    include_package_data = True,
    platforms = 'any',
    test_suite = 'alteracloud.test.tests',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: System :: Distributed Computing',     
        ],
    extras_require = {
        'testing': ['pytest'],
    }
)
