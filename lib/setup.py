# -*- coding: utf-8 -*-

# This file is part of djubby <http://djubby.googlecode.com/>,
# a Linked Data frontend for SPARQL endpoints for the Django Web framework
#
# Copyright (C) 2010 Sergio Fernández
#
# Djubby is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Djubby is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Djubby. If not, see <http://www.gnu.org/licenses/>.


from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
 
setup(
      name             = "djubby",
      version          =  "0.1.9-dev",
      description      = "A Linked Data frontend for SPARQL endpoints for Django",
      license          = "GNU Library or Lesser General Public License (LGPL) v3",
      author           = "Sergio Fernández",
      author_email     = "sergio@wikier.org",
      url              = "https://github.com/wikier/djubby",
      download_url     = "https://github.com/wikier/djubby/releases",
      platforms        = ["any"],
      packages         = ["djubby"],
      requires         = ["rdflib", "SPARQLWrapper", "django", "mimeparse"], 
      install_requires = ["rdflib >= 4.1.0", "SPARQLWrapper >= 1.6.4", "django >= 1.1.0", "mimeparse >= 0.1.2"],
      classifiers      = [
                            "Development Status :: 4 - Beta ",
                            "Intended Audience :: Developers",
                            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                            "Operating System :: OS Independent",
                            "Programming Language :: Python :: 2.6",
                         ],
      keywords         = "python django rdf sparql linkeddata",
      scripts          = ["ez_setup.py"],
      data_files       = [ ("tpl", ["tpl/resource.tpl"]) ]
)

