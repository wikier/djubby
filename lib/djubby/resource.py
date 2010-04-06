# -*- coding: utf-8 -*-

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

