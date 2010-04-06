# -*- coding: utf-8 -*-

from configuration import Configuration
import mimeparse
from sets import Set
from django.http import HttpResponseRedirect

formats = {
            "data" : [ "application/rdf+xml" ],
            "page" : [ "text/html", "application/xhtml+xml" ]

          }

def get_supported_prefixes():
    return formats.keys()

def get_supported_formats():
    f = Set()
    for l in formats.itervalues():
        f = f.union(Set(l))
    return list(f)

def get_mimetype(prefix):
    if (not prefix in formats):
        prefix = "data"
    return formats[prefix][0]

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

def url_handler(ref):
    uri = None
    prefix = None
    conf = Configuration()
    base = conf.get_value("datasetBase")
    if (ref.startswith("http://")):
        if (not ref.startswith(base)):
            raise ValueError("Invalid URI for this dataset")
        else:
            ref = ref[len(base):]

    splitted = ref.split("/")
    if (splitted[0] in get_supported_prefixes()):
        prefix = splitted[0]
        uri = base + "/".join(splitted[1:])
    else:
        prefix = None
        uri = base + ref
    return uri, prefix

class Http303(HttpResponseRedirect):
    status_code = 303

