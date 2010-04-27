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
from configuration import Configuration
from SPARQLWrapper import SPARQLWrapper, JSON
from django.template import Template, Context
import rdf
import ns
from uri import URI, uri2curie, uri2str, quote
from rdflib import URIRef
from rdflib import Literal
from http import get_document_url

class Resource:

    queries = {
                "ask"      : "ASK { GRAPH <%s> { <%s> ?p ?o } }",
                "describe" : "DESCRIBE <%s> FROM <%s>"
              }

    def __init__(self, uri):
        logging.debug("Trying to build resource with URI <%s>..." % uri)
        self.uri = uri2str(uri)
        self.conf = Configuration()
        self.graph = self.conf.graph
        self.endpoint = self.conf.endpoint
        if (self.__ask__()):
            logging.info("Successfully found the resource with URI <%s> on this dataset" % self.uri)
        else:
            #FIXME: patch to support incosistencies on the URIs
            cleanuri = self.uri
            self.uri = quote(self.uri)
            logging.debug("Not found on the first try, trying the encoded URI  <%s>..." % self.uri)
            if (self.__ask__()):
                logging.info("Successfully found the resource with URI <%s> on this dataset" % self.uri)
            else:
                raise ValueError("Resource with URI <%s> not found on this dataset" % self.uri)            

    def get_triples(self):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.queries["describe"] % (self.uri, self.graph))
        g = sparql.query().convert()
        logging.debug("Returning %d triples describing resource <%s>" % (len(g), self.uri))
        #FIXME: enrich with metadata
        for prefix, namespace in self.conf.data.namespaces():
            g.bind(prefix, namespace) 
        return g

    def get_uri(self):
        return uri

    def get_data_url(self):
        return get_document_url(self.uri, "data")

    def get_page_url(self):
        return get_document_url(self.uri, "page")

    def get_data(self):
        return get_data_xml()

    def get_data_xml(self):
        g = self.get_triples()
        return g.serialize(format="pretty-xml")

    def get_data_n3(self):
        g = self.get_triples()
        return g.serialize(format="n3")

    def get_page(self):
        return get_page_html()

    def get_page_html(self):
        g = self.get_triples()
        tpl = Template(self.__read_template__())

        data = {}
        data["uri"] = URI(self.uri)
        lang = self.conf.get_value("defaultLanguage")
        data["lang"] = lang
        label = rdf.get_value(g, self.uri, ns.rdfs["label"], lang)
        if (len(label)>0):
            data["label"] = label
        else:
            data["label"] = self.uri
        datasetBase = self.conf.get_value("datasetBase")
        webBase = self.conf.get_value("webBase")
        data["data"]  = self.get_data_url()
        data["project"] = self.conf.get_value("projectName")
        data["homelink"] = self.conf.get_value("projectHomepage")
        data["endpoint"] = self.conf.get_value("sparqlEndpoint")
        depiction = rdf.get_value(g, self.uri, ns.foaf["depiction"])
        if (len(depiction)>0):
            data["depiction"] = depiction

        data["rows"] = self.__get_rows__(g)

        ctx = Context(data)
        return tpl.render(ctx)

    def __ask__(self):
        sparql = SPARQLWrapper(self.endpoint)
        query = self.queries["ask"] % (self.graph, self.uri)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if (results.has_key("boolean")):
            # expected answer according SPARQL Protocol
            if (results["boolean"]):
                return True
        elif (results.has_key("results") and results["results"].has_key("bindings") and len(results["results"]["bindings"])>0):
            # I don't know why, but virtuoso sometimes uses __ask_retval
            # http://docs.openlinksw.com/virtuoso/rdfsparql.html
            if (bool(results["results"]["bindings"][0]["__ask_retval"]["value"])):
                return True
        else:
            return False
        return False

    def __get_rows__(self, g):
        rows = {}
        for p, o in rdf.get_predicates(g, self.uri):
            prop = URI(p)
            if (not rows.has_key(prop)):
                rows[prop] = []
            if (type(o) == URIRef):
                rows[prop].append(URI(o))
            elif (type(o) == Literal):
                item = {}
                item["literal"] = unicode(o)
                if (o.language):
                    item["language"] = o.language
                if (o.datatype):
                    item["datatype"] = uri2curie(o.datatype, self.conf.data.namespaces())
                rows[prop].append(item)
            else:
                rows[prop].append(o)
        return rows

    def __read_template__(self, name="resource"):
        path = "%s/../tpl/%s.tpl" % (os.path.dirname(__file__), name)
        logging.debug("Reading template '%s' from %s" % (name, path))
        f = open(path, "r")
        content = f.read()
        f.close()
        return content

