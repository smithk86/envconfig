#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='envconfig',
    version='0.1',
    description="define required properties and set via defaults or environment variables",
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    url='https://github.com/smithk86/envconfig',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    extras_require={
        'yaml':  ['PyYAML==3.13'],
        'dateparser': ['dateparser==0.7.0'],
    }
)