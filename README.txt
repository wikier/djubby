Djubby: a Pubby clone for Django, a Linked Data frontend for SPARQL endpoints 
=============================================================================

Djubby is a Python implementation of pubby, a Linked Data frontend for SPARQL 
endpoints for the Django Web framework.

More information at: http://djubby.googlecode.com/


Authors:
-------
    *  Sergio Fernández <sergio@wikier.org>


Features:
--------
    * Provides a Linked Data interface to local or remote SPARQL protocol servers
    * Provides dereferenceable URIs by rewriting URIs found in the SPARQL-exposed dataset into the djubby server's namespace
    * Takes care of handling 303 redirects and content negotiation
    * Compatible with the Django Web framework

Planned:
    * Provides a simple HTML interface showing the data available about each resource
    * Includes a metadata extension to add metadata to the provided data


Dependencies:
------------
    * RDFLIB >= 2.4.0
    * SPARQLWrapper >= 1.3.2
    * Django >= 1.1.0
    * mimeparse >= 0.1.2


Install:
-------
    cd lib/
    sudo python setup.py install

