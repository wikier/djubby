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

import logging
from django.http import HttpResponse, Http404
from configuration import Configuration
from resource import Resource
from http import Http303, Http307, Http405, Http501, get_preferred_prefix, get_preferred_output, get_mimetype, url_handler
from urllib2 import URLError

def dispatcher(request, ref=None):
    conf = Configuration()
    method = request.method
    logging.debug("Dispatching %s request on '%s'..." % (method, ref))
    try:
        dispatch = eval("dispatcher_%ss" % method.lower())
        return dispatch(request, ref, conf)
    except NameError:
        msg = "dispatcher not found for %s requests" % method
        logging.error(msg)
        raise Http405(msg)

def dispatcher_gets(request, ref, conf):
    if (ref == None or len(ref) == 0):
        index = conf.get_value("indexResource")
        index = index.replace(conf.get_value("datasetBase"), conf.get_value("webBase"))
        logging.debug("Redirecting to the index resource...")
        return Http307(index)
    else:
        try:
            uri, prefix = url_handler(ref, conf)
            resource = Resource(uri)
        except ValueError, ve:
            logging.error("Error processing request for '%s': %s" % (ref, str(ve)))
            raise Http404(ve)
        except URLError, ue:
            logging.error("Error retrieving data for '%s': %s" % (ref, str(ue)))
            raise Http404(ue)

        if (prefix == None):
            prefix = get_preferred_prefix(request)
            get_url = getattr(resource, "get_%s_url" % prefix)
            url = get_url()
            logging.debug("Redirecting to the %s representation of %s: %s" % (prefix, uri, url))
            return Http303(url)
        else:         
            output = get_preferred_output(request, prefix)
            func = getattr(resource, "get_%s_%s" % (prefix, output))
            mimetype = get_mimetype(prefix, output)            
            logging.debug("Returning the %s representation of %s serialized as %s" % (prefix, uri, output))       
            return HttpResponse(func(), mimetype=mimetype)

def dispatcher_posts(request, ref, conf):
    graph = ""
    if (ref == None or len(ref) == 0):
        logging.debug("no explicit graph, so using the default one")
        graph = conf.get_value("sparqlDefaultGraph")
    else:
        graph, prefix = url_handler(ref, conf)
        print graph, prefix
    raise Http501("not yet implemented")

