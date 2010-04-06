# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from configuration import Configuration
from resource import Resource
from http import Http303, get_preferred_prefix, get_mimetype, url_handler
import logging

def dispatcher(request, ref=None):
    logging.debug("dispatching '%s'..." % ref)
    if (ref == None or len(ref) == 0):
        conf = Configuration()
        index = conf.get_value("indexResource")
        return HttpResponseRedirect(index)
    else:
        try:
            uri, prefix = url_handler(ref)
            resource = Resource(uri)
        except ValueError, ve:
            raise Http404(ve)

        if (prefix == None):
            return Http303("%s/%s" % (get_preferred_prefix(request),ref))
        else:
            #FIXME: HTML renderization
            return HttpResponse(resource.get_data(), mimetype=get_mimetype(prefix))

