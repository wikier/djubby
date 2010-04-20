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

from configuration import Configuration
import mimeparse
from sets import Set
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

formats = {
            "data" : { "default":"application/rdf+xml", "xml":"application/rdf+xml", "n3":"text/n3" },
            "page" : { "default":"text/html", "html":"text/html", "xhtml":"application/xhtml+xml" }

          }

def get_supported_prefixes():
    return formats.keys()

def get_supported_formats():
    fs = Set()
    for f in formats.itervalues():
        for m in f.itervalues():
            fs.add(m)
    return list(fs)

def get_supported_outputs():
    outputs = Set()
    for f in formats.itervalues():
        for o in f.iterkeys():
            if (not o == "default"):
                outputs.add(o)
    return list(outputs)

def get_mimetype(prefix, output):
    if (not prefix in formats):
        prefix = "data"
    if (not output in formats[prefix]):
        output = "default"
    return formats[prefix][output]

def get_prefix(mimetype):
    for prefix, mimes in formats.items():
        if mimetype in mimes:
            return prefix
    return "data"

def get_preferred_format(request):
    try:
        accept = request.META["HTTP_ACCEPT"]
    except KeyError:
        accept = formats["data"]
    return mimeparse.best_match(get_supported_formats(), accept)

def get_preferred_prefix(request):
    return get_prefix(get_preferred_format(request))

def get_preferred_output(request, prefix):
    if (prefix == "page"):
        return "html"
    else:
        try:
            output = request.GET["output"]
            if (output in get_supported_outputs()):
                return output
            else:
                return "xml"
        except MultiValueDictKeyError:
            return "xml"

def url_handler(ref):
    uri = None
    prefix = None
    conf = Configuration()
    datasetBase = conf.get_value("datasetBase")
    webBase = conf.get_value("webBase")

    splitted = ref.split("/")
    if (splitted[0] in get_supported_prefixes()):
        prefix = splitted[0]
        uri = datasetBase + "/".join(splitted[1:])
    else:
        prefix = None
        uri = datasetBase + ref
    return uri, prefix

class Http303(HttpResponseRedirect):
    status_code = 303

