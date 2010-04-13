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

from rdflib import URIRef
import logging

def get_values(graph, subject=None, predicate=None):
    return graph.objects(subject=str2uri(subject), predicate=predicate)

def get_value(graph, subject=None, predicate=None):
    try:
        return str(get_values(graph, subject, predicate).next())
    except StopIteration:
        return ""

def get_predicates(graph, subject=None):
    return graph.predicate_objects(str2uri(subject))

def str2uri(uri):
    if (type(uri)==str or type(uri)==unicode):
        return URIRef(uri)
    else:
        return uri

