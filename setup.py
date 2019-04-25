# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

setup(
    name='qnap', 
    description='Python binding for QNAP File Station API', 
    version='0.1', 
    author='Satoshi Murashige', 
    author_email='murashige.satoshi.mi1 [at] is.naist.jp', 
    url='https://github.com/eqs/qnap', 
    install_requires=['requests'], 
    packages=find_packages()
)

