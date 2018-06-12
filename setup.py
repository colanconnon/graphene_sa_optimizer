# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='graphene_sa_optimizer',
    version='0.0.4',
    author='Colan Connon',
    author_email='cconnon11@gmail.com',
    description='Use GraphQL and SQL Alchemy for efficient database access.',
    license='MIT',
    keywords='graphene sqlalchemy flask graphql',
    url='https://github.com/colanconnon/graphene_sa_optimizer',
    packages=['graphene_sa_optimizer'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',  
    ],
)