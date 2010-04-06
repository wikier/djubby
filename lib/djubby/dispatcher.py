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

import logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from configuration import Configuration
from resource import Resource
from http import Http303, get_preferred_prefix, get_mimetype, url_handler

def dispatcher(request, ref=None):
    logging.debug("Dispatching request on '%s'..." % ref)
    if (ref == None or len(ref) == 0):
        conf = Configuration()
        index = conf.get_value("indexResource")
        logging.debug("Redirecting to the index resource...")
        return HttpResponseRedirect(index)
    else:
        try:
            uri, prefix = url_handler(ref)
            resource = Resource(uri)
        except ValueError, ve:
            logging.error("Error processing URI <%s>: %s" % (ref, str(ve)))
            raise Http404(ve)

        if (prefix == None):
            prefix = get_preferred_prefix(request)
            logging.debug("Redirecting to the %s representation of %s" % (prefix, uri))
            return Http303("%s/%s" % (prefix, ref))
        else:
            logging.debug("Returning the %s representation of %s" % (prefix, uri))         
            return HttpResponse(resource.get_data(), mimetype=get_mimetype(prefix)) #FIXME: HTML renderization

