#!/usr/bin/env python
from distutils.core import setup


VERSION = __import__('django_badbrowser').VERSION

import os
long_description = open(os.path.join(os.path.dirname(__file__), 'README.textile')).read()

setup(
      name='django-badbrowser',
      version=VERSION,
      url='http://github.com/adamcharnock/django-badbrowser',
      download_url='git@github.com:adamcharnock/django-badbrowser.git',
      description='Browser detection (including browser upgrade notices) for Django',
      long_description=long_description,
      author='Adam Charnock',
      author_email='adam@playnice.ly',
      platforms=['any'],
      license='MIT',
      packages=[
        'django_badbrowser',
        ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        ],
      include_package_data=True,
)
