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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Djubby. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from rdflib.Graph import ConjunctiveGraph
from rdflib import Namespace

class Configuration:

    __shared_state = { "data" : None, "path" : None, "ns" : Namespace("http://richard.cyganiak.de/2007/pubby/config.rdf#") }

    def __init__(self, path=None):
        self.__dict__ = self.__shared_state
        if (self.data == None):
            if (path == None):
                self.path = settings.DJUBBY_CONF
            else:
                self.path = path
            print "reading djubby's configuration..."
            data = ConjunctiveGraph()
            data.load(path, format='n3')
            data.bind("conf", self.ns)  
            self.data = data
            self.__class__.__dict__['_Configuration__shared_state']["data"] = data #FIXME

    def get_values(self, prop):
        return self.data.objects(subject=None, predicate=self.ns[prop])

    def get_value(self, prop):
        return str(self.get_values(prop).next())

