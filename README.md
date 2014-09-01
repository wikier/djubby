
= Djubby: a Pubby clone for Django, a Linked Data frontend for SPARQL endpoints =

Djubby is a Linked Data frontend for SPARQL endpoints for the Django Web framework.
It's quite inspired by Richard Cyganiak's Pubby, and with the exception of the HTML
style, all the code has beed written from scratch due the many differences between 
languages (Java vs. Python) and the frameworks (JavaEE vs. Django).

More information at: https://github.com/wikier/djubby

== Authors ==

*  Sergio Fernández <sergio@wikier.org>

== Features ==

* Provides a Linked Data interface to local or remote SPARQL protocol servers.
* Provides dereferenceable URIs by rewriting URIs found in the SPARQL-exposed dataset into the djubby server's namespace.
* Provides a simple HTML interface showing the data available about each resource.
* Takes care of handling 303 redirects and content negotiation.
* Compatible with the Django Web framework.

Planned: Include a metadata extension to add metadata to the provided data.

== Limitations ==

* Only works for SPARQL endpoint that can answer ASK and DESCRIBE queries.
* Multiple dataset support may not work as expected, so it is recommended to simply set up a separate djubby instance for each dataset.


== Dependencies ==

* RDFLib >= 2.4.0
* SPARQLWrapper >= 1.3.2
* Django >= 1.1.0
* mimeparse >= 0.1.2

== Usage ==

=== Installation ===

    cd lib/
    sudo python setup.py install

== License: ==

GNU Library or Lesser General Public License (LGPL) v3, http://www.gnu.org/licenses/lgpl.html
