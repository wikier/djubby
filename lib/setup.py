# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
 
setup(
      name='djubby',
      version='0.0.1',
      description='A Pubby clone for Django, a Linked Data frontend for SPARQL endpoints',
      license = 'GNU Library or Lesser General Public License (LGPL) v3',
      author='Sergio Fernández',
      author_email='sergio@wikier.org',
      url = 'http://djubby.googlecode.com/',
      download_url = '',
      platforms = ['any'],
      packages=['djubby'],
      requires=['rdflib', 'SPARQLWrapper', 'django', 'mimeparse'], 
      install_requires=['rdflib == 2.4.0', 'SPARQLWrapper == 1.3.2', 'django == 1.0.2-final', 'mimeparse == 0.1.2'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
      ],
      keywords = 'python django rdf sparql linkeddata',
      scripts = ['ez_setup.py'],
)

