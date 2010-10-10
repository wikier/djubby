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

from rdflib import URIRef
from rdflib import ConjunctiveGraph
from cStringIO import StringIO

#FIXME: duplicate function because circular import
def str2uri(uri):
    if (type(uri)==str or type(uri)==unicode):
        return URIRef(uri)
    else:
        return uri

def get_values(graph, subject=None, predicate=None):
    return graph.objects(subject=str2uri(subject), predicate=predicate)

def get_value(graph, subject=None, predicate=None, lang=None):
    if (lang == None):
        try:
            return str(get_values(graph, subject, predicate).next())
        except StopIteration:
            return ""
    else:
        values = get_values(graph, subject, predicate)
        for value in values:
            if (value.language == lang):
                return value
        return ""

def get_predicates(graph, subject=None):
    return graph.predicate_objects(str2uri(subject))

def translate(graph, fout="nt", base=None):
    return graph.serialize(None, fout, base)    

def translate_old(src, uri, fin="xml", fout="nt"):
    g = parse_rdf(src, uri, fin)
    return g.serialize(None, fout, uri)    

def rdf2triplepatterns(src, uri, format="xml"):
    return translate(src, uri, format, "nt")

def graph2triplepatterns(graph, base=None):
    return translate(graph, "nt", base)

def parse_rdf(data, uri, format="xml"):
    g = ConjunctiveGraph()
    g.load(StringIO(data), uri, format)
    return g

