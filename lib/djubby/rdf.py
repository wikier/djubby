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

class URI:

    def __init__(self, uri, label=None):
        if (type(uri)==URIRef):
            self.uri = unicode(uri)
        else:
            self.uri = uri
        self.label = label

    def __str__(self):
        return self.uri

    def __cmp__(self, o):
        return cmp(self.uri, o.uri)

    def __eq__(self, o):
        return self.uri.__eq__(o.uri)

    def __hash__(self):
        return self.uri.__hash__()

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

def str2uri(uri):
    if (type(uri)==str or type(uri)==unicode):
        return URIRef(uri)
    else:
        return uri

def uri2curie(uri, namespaces):
    url, fragment = splitUri(uri)
    for prefix, ns in namespaces: #improve the performace of this operation       
        if (unicode(ns) == url):
            return "%s:%s" % (prefix, fragment)
    return uri

def splitUri(uri):
    if ("#" in uri):
        splitted = uri.split("#")
        return ("%s#"%splitted[0], splitted[1])
    else:
        splitted = uri.split("/")
        return ("/".join(splitted[:-1])+"/", splitted[-1])

