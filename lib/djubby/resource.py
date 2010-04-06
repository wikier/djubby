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

from configuration import Configuration
from SPARQLWrapper import SPARQLWrapper, JSON

class Resource:

    queries = {
                "ask"      : "ASK { GRAPH <%s> { <%s> ?p ?o } }",
                "describe" : "DESCRIBE <%s> FROM <%s>"
              }

    def __init__(self, uri):
        self.uri = uri
        conf = Configuration()
        self.graph = conf.get_value("sparqlDefaultGraph")
        self.endpoint = conf.get_value("sparqlEndpoint")
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.queries["ask"] % (self.graph, self.uri))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if (not results["boolean"]):
            raise ValueError("URI not found on this dataset")

    def get_triples(self):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.queries["describe"] % (self.uri, self.graph))
        return sparql.query().convert()

    def get_data(self):
        g = self.get_triples()
        return g.serialize(format="pretty-xml")

