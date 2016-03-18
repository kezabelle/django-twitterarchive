#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


HERE = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def make_readme(root_path):
    consider_files = ('README.rst', 'LICENSE', 'CHANGELOG', 'CONTRIBUTORS')
    for filename in consider_files:
        filepath = os.path.realpath(os.path.join(root_path, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode='r') as f:
                yield f.read()


LONG_DESCRIPTION = "\r\n\r\n----\r\n\r\n".join(make_readme(HERE))


setup(
    name='django-twitterarchive',
    version='0.1.0',
    author='Keryn Knight',
    author_email='python-package@kerynknight.com',
    description="Django management command + model for reading a twitter archive",
    long_description=LONG_DESCRIPTION,
    packages=[
        'twitterarchive',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.0',
        'twitter-text-python>=1.1.0',
    ],
    tests_require=[
        "model-mommy>=1.2.2",
        'pytest>=2.6.4',
        'pytest-cov>=1.8.1',
        'pytest-django>=2.8.0',
        'pytest-mock>=0.11.0',
        'pytest-remove-stale-bytecode>=1.0',
    ],
    cmdclass={'test': PyTest},
    zip_safe=False,
    keywords='django twitter archive management command',
    license="BSD License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
