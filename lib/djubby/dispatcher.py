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
from http import Http303, Http307, Http405, Http406, Http500, Http501, get_preferred_prefix, get_preferred_output, get_mimetype, url_handler, parse_post_request
from sparql import insert
from rdf import graph2triplepatterns
from urllib2 import URLError

def dispatcher(request, ref=None):
    conf = Configuration()
    method = request.method
    logging.debug("Dispatching %s request on '%s'..." % (method, ref))
    try:
        dispatch = eval("dispatcher_%ss" % method.lower())
    except NameError, ne:
        msg = "dispatcher not found for %s requests" % method
        logging.error(msg)
        raise Http405(msg, ne)
    return dispatch(request, ref, conf)

def dispatcher_gets(request, ref, conf):
    if (ref == None or len(ref) == 0):
        index = conf.get_value("indexResource")
        index = index.replace(conf.get_value("datasetBase"), conf.get_value("webBase"))
        logging.debug("Redirecting to the index resource...")
        return Http307(index)
    else:
        try:
            uri, prefix = url_handler(request, ref, conf)
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
    #see http://code.google.com/p/djubby/wiki/ReadWriteLinkedData#Graph_Identification
    #graph = None
    #if (ref == None or len(ref) == 0):
    #    logging.debug("No explicit graph, so using the default one")
    #    graph = conf.get_value("sparqlDefaultGraph")
    #else:
    #    graph = url_handler(request, ref, conf)
    #    logging.debug("Using <%s> graph" % graph)

    graph = conf.get_value("sparqlDefaultGraph")
    uri = None
    if (ref == None or len(ref) == 0):
        logging.debug("No explicit URI, so using the base one")
        uri = conf.get_value("datasetBase"),
    else:
        uri = url_handler(request, ref, conf)
        logging.debug("Using <%s> as base URI" % uri)

    data = None
    try:
        data = parse_post_request(request, uri) 
    except Exception, e:
        logging.error("Unable to parse POST request as RDF: %s" % e)
        raise Http406(e)

    if (len(data)>300):
        logging.warn("Huge number of triples would generate a too big query for many sparql engines")

    try:
        result = insert(conf.endpoint, graph, graph2triplepatterns(data, uri))
    except URLError, e:
        logging.error("Unable to insert data to the endpoint: %s" % e)
        raise Http500(e)

    logging.info("Successfully inserted data")
    if (hasattr(result, "toxml")):
        return HttpResponse(result.toxml(), mimetype="application/xml") 
    else:
        return HttpResponse(result, mimetype="text/plain")

