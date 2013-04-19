#!/usr/bin/env python
from distutils.core import setup

setup(name='django-blinks',
      version='0.1',
      description='Django app for adding and managing site relative bookmarks',
      author='AGoodId',
      author_email='teknik@agoodid.se',
      url='http://github.com/AGoodId/django-blinks/',
      packages=['blinks', 'blinks.templatetags'],
      license='BSD',
      include_package_data = False,
      zip_safe = False,
      classifiers = [
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Environment :: Web Environment',
          'Framework :: Django',
      ],
)
