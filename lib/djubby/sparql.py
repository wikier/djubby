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

from SPARQLWrapper import SPARQLWrapper, JSON

queries = {
            "ask"      : "ASK { GRAPH <%s> { <%s> ?p ?o } }",
            "describe" : "DESCRIBE <%s> FROM <%s>"
          }

def ask(enpoint, graph, uri):
    sparql = SPARQLWrapper(endpoint)
    query = queries["ask"] % (graph, uri)
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

def describe(enpoint, graph, uri):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(queries["describe"] % (uri, graph))
    g = sparql.query().convert()
