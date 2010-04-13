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
    if (type(subject)==str or type(subject)==unicode):
        subject = URIRef(subject)
    return graph.objects(subject=subject, predicate=predicate)

def get_value(graph, subject=None, predicate=None):
    try:
        return str(get_values(graph, subject, predicate).next())
    except StopIteration:
        return ""

