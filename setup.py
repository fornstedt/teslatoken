# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='teslatoken',
    version='0.1.3',
    description='Tool to create authorization tokens for Tesla cars.',
    long_description=readme,
    license=license,
    keywords='tesla authorization token',
    py_modules=['teslatoken'],
    install_requires = ['certifi'],
    author='Eric Fornstedt',
    author_email='eric.fornstedt@gmail.com',
    url='https://github.com/eric1980/teslatoken',
    entry_points={'console_scripts': ['teslatoken=teslatoken:main']}
)
