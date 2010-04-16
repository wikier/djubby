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

import os
import logging
from django.conf import settings
from rdflib.Graph import ConjunctiveGraph
import rdf
import ns

class Configuration:
    """Configuration using the Borg design pattern"""

    __shared_state = { "data" : None, "path" : None, "graph" : None, "endpoint" : None}

    def __init__(self, path=None):
        self.__dict__ = self.__shared_state
        if (self.data == None):
            if (path == None):
                raise ValueError("djubby's configuration MUST be initialized a first time, read http://code.google.com/p/djubby/wiki/GettingStarted")
            else:
                self.path = os.path.abspath(path)
                logging.debug("Reading djubby's configuration from %s..." % self.path)
                if (not os.path.exists(self.path)):
                    raise ValueError("Not found a proper file at '%s' with a configuration for djubby. Please, provide a right path" % self.path)

                data = ConjunctiveGraph()
                data.bind("conf", ns.config) 
                try:
                    data.load(path, format='n3') 
                except Exception, e:
                    raise ValueError("Not found a proper N3 file at '%s' with a configuration for djubby. Please, provide a valid N3 file" % self.path)

                self.data = data
                try:
                    self.graph = self.get_value("sparqlDefaultGraph")
                    self.endpoint = self.get_value("sparqlEndpoint")
                except Exception, e:
                    raise ValueError("Not found the graph not the endpoint that it's supposed djubby have to query. Please, provide a right donfiguration")

                logging.info("Using <%s> as default graph to query the endpoint <%s>" % (self.graph, self.endpoint))
                self.__class__.__dict__['_Configuration__shared_state']["data"] = data #FIXME

    def get_values(self, prop):
        return rdf.get_values(self.data, predicate=ns.config[prop])

    def get_value(self, prop):
        return rdf.get_value(self.data, predicate=ns.config[prop])

