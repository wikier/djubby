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
from configuration import Configuration
from SPARQLWrapper import SPARQLWrapper, JSON
from django.template import Template, Context
import rdf
import ns
from rdflib import URIRef
from rdflib import Literal

class Resource:

    queries = {
                "ask"      : "ASK { GRAPH <%s> { <%s> ?p ?o } }",
                "describe" : "DESCRIBE <%s> FROM <%s>"
              }

    def __init__(self, uri):
        logging.debug("trying to build resource with URI <%s>..." % uri)
        self.uri = uri
        conf = Configuration()
        self.graph = conf.get_value("sparqlDefaultGraph")
        self.endpoint = conf.get_value("sparqlEndpoint")
        sparql = SPARQLWrapper(self.endpoint)
        query = self.queries["ask"] % (self.graph, self.uri)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if (results.has_key("boolean")):
            # expected answer according SPARQL Protocol
            if (not results["boolean"]):
                raise ValueError("URI not found on this dataset")
        elif (results.has_key("results") and results["results"].has_key("bindings") and len(results["results"]["bindings"])>0):
            # I don't know why, but virtuoso sometimes uses __ask_retval
            # http://docs.openlinksw.com/virtuoso/rdfsparql.html
            if (not bool(results["results"]["bindings"][0]["__ask_retval"]["value"])):
                raise ValueError("URI not found on this dataset")
        else:
            raise ValueError("URI not found on this dataset")

    def get_triples(self):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.queries["describe"] % (self.uri, self.graph))
        g = sparql.query().convert()
        logging.debug("Returning %d triples describing resource <%s>" % (len(g), self.uri))
        #FIXME: enrich with metadata
        return g

    def get_data(self):
        g = self.get_triples()
        return g.serialize(format="pretty-xml")

    def get_page(self):
        g = self.get_triples()
        tpl = Template(self.__read_template__())
        conf = Configuration()

        data = {}
        data["uri"] = self.uri
        lang = conf.get_value("defaultLanguage")
        label = rdf.get_value(g, self.uri, ns.rdfs["label"], lang)
        if (len(label)>0):
            data["label"] = label
        else:
            data["label"] = self.uri
        datasetBase = conf.get_value("datasetBase")
        webBase = conf.get_value("webBase")
        data["data"]  = self.uri.replace(datasetBase, "%s%s/" % (webBase, "data"))
        data["project"] = conf.get_value("projectName")
        data["homelink"] = conf.get_value("projectHomepage")
        data["endpoint"] = conf.get_value("sparqlEndpoint")
        depiction = rdf.get_value(g, self.uri, ns.foaf["depiction"])
        if (len(depiction)>0):
            data["depiction"] = depiction

        data["rows"] = self.__get_rows__(g)

        ctx = Context(data)
        return tpl.render(ctx)

    def __get_rows__(self, g):
        rows = {}
        for p, o in rdf.get_predicates(g, self.uri):
            p = str(p)
            if (not rows.has_key(p)):
                rows[p] = []
            if (type(o) == URIRef):
                item = {}
                item["uri"] = unicode(o)
                item["label"] = unicode(o) #FIXME: CURIE
                rows[p].append(item)
            elif (type(o) == Literal):
                item = {}
                item["literal"] = unicode(o)
                if (o.language):
                    item["language"] = o.language
                #FIXME: xsd datatypes
                rows[p].append(item)
            else:
                rows[p].append(o)
        return rows

    def __read_template__(self, name="resource"):
        path = "%s/../tpl/%s.tpl" % (os.path.dirname(__file__), name)
        logging.debug("Reading template '%s' from %s" % (name, path))
        f = open(path, "r")
        content = f.read()
        f.close()
        return content

