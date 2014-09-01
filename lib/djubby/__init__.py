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
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Djubby. If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.1.9-dev"
__authors__ = "Sergio Fernández"
__license__ = "GNU Library or Lesser General Public License (LGPL) v3"
__contact__ = "sergio@wikier.org"
__date__    = "2014-09-01"
__agent__   = "djubby %s (http://github.com/wikier/djubby)" % __version__

# Some common stuff for network:
import socket
import urllib2
socket.setdefaulttimeout(10)

# Making imports easier for users:
from dispatcher import dispatcher
from configuration import Configuration

