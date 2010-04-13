# -*- coding: utf-8 -*-

# This file is part of Djubby.
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

import os
import logging
from django.conf import settings
from rdflib.Graph import ConjunctiveGraph
import rdf
import ns

class Configuration:
    """Configuration using the Borg design pattern"""

    __shared_state = { "data" : None, "path" : None }

    def __init__(self, path=None):
        self.__dict__ = self.__shared_state
        if (self.data == None):
            if (path == None):
                raise ValueError("djubby's configuration MUST be initialized a first time, read http://code.google.com/p/djubby/wiki/GettingStarted")
            else:
                logging.debug("reading djubby's configuration from %s" % os.path.abspath(path))
                data = ConjunctiveGraph()
                data.load(path, format='n3')
                data.bind("conf", ns.config)  
                self.data = data
                self.__class__.__dict__['_Configuration__shared_state']["data"] = data #FIXME

    def get_values(self, prop):
        return rdf.get_values(self.data, predicate=ns.config[prop])

    def get_value(self, prop):
        return rdf.get_value(self.data, predicate=ns.config[prop])

