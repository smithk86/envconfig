#!/usr/bin/env python

import os.path

from setuptools import setup


dir_ = os.path.abspath(os.path.dirname(__file__))
# get the version to include in setup()
with open(f'{dir_}/envprops.py') as fh:
    for line in fh:
        if '__VERSION__' in line:
            exec(line)
# get long description from README.md
with open(f'{dir_}/README.md') as fh:
    long_description = fh.read()


setup(
    name='pyenvprops',
    version=__VERSION__,
    license='MIT',
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    url='https://github.com/smithk86/envprops',
    py_modules=['envprops'],
    description='define and set application properties using a file and enviornment variables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    extras_require={
        'yaml': ['PyYAML'],
        'date': ['dateparser'],
    }
)
