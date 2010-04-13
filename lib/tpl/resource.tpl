<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>{{label}} | {{project}}</title>
    <link rel="alternate" type="application/rdf+xml" href="{{data}}" title="RDF" />
    <style type="text/css">
		html { margin: 0; padding: 0; }
		body { font-family: sans-serif; font-size: 80%; margin: 0; padding: 1.2em 2em; }
		#rdficon { float: right; position: relative; top: -28px; }
		#header { border-bottom: 2px solid #696; margin: 0 0 1.2em; padding: 0 0 0.3em; }
		#footer { border-top: 2px solid #696; margin: 1.2em 0 0; padding: 0.3em 0 0; }
		#homelink { display: inline; }
		#homelink, #homelink a { color: #666; }
		#homelink a { font-weight: bold; text-decoration: none; }
		#homelink a:hover { color: red; text-decoration: underline; }
		h1 { display: inline; font-weight: normal; font-size: 200%; margin: 0; text-align: left; }
		h2 { font-weight: normal; font-size: 124%; margin: 1.2em 0 0.2em; }
		.page-resource-uri { font-size: 124%; margin: 0.2em 0; }
		.page-resource-uri a { color: black; text-decoration: none; }
		.page-resource-uri a:hover { color: red; text-decoration: underline; }
		a.sparql-uri { color: black; text-decoration: none; }
		a.sparql-uri:hover { color: red; text-decoration: underline; }
		img { border: none; }
		table.description { border-collapse: collapse; clear: left; font-size: 100%; margin: 0 0 1em; width: 100%; }
		table.description th { background: white; text-align: left; }
		table.description td, table.description th { line-height: 1.2em; padding: 0.2em 0.4em; vertical-align: top; }
		table.description ul { margin: 0; padding-left: 0em; }
		table.description li { list-style-type: square; }
		.uri { white-space: nowrap; }
		.uri a, a.uri { text-decoration: none; }
		.unbound { color: #888; }
		table.description a small, .metadata-table a small  { font-size: 100%; color: #55a; }
		table.description small, .metadata-table a small  { font-size: 100%; color: #666; }
		table.description .property { white-space: nowrap; }
		h1, h2 { color: #810; }
		body { background: #cec; }
		table.description .odd td { background: #d4f6d4; }
		table.description .even td { background: #f0fcf0; }
		.image { background: white; float: left; margin: 0 1.5em 1.5em 0; padding: 2px; }
		a.expander { text-decoration: none; }
		
		.metadata-label {
			font-size: 100%;
			background: #f0fcf0;
			padding: 3px;
		}
		
		.metadata-table {
			font-size: 100%;
			border-left: 3px solid #f0fcf0;
			border-bottom: 3px solid #f0fcf0;
			border-right: 3px solid #f0fcf0;
			background: #d4f6d4;
			border-top: 0px solid none;
			margin: 0px;
		}
		
		.metadata-table td {
			padding: 3px;
		}
    </style>
  </head>
  <body onLoad="init();">

    <div id="header">
      <div>
        <h1 id="title">{{label}}</h1>
        <div id="homelink">at <a href="{{homelink}}">{{project}}</a></div>
      </div>
      <div class="page-resource-uri"><a href="{{uri}}">{{uri}}</a></div>
      <div id="rdficon"><a href="{{data}}" title="RDF data"><img src="http://www.w3.org/RDF/icons/rdf_flyer.24" alt="[This page as RDF]" /></a></div>

    </div>

    {% if depiction %}
        <div class="image"><img src="{{depiction}}" alt="Depiction of {{label}}" /></div>
    {% endif %}

    <table class="description">
      <tr>
        <th width="25%">Property</th>
        <th>Value/s</th>
      </tr>
      {% for prop, values in rows.items %}
      <tr>
        <td class="property">
          <a class="uri" href="{{prop}}" title="{{prop}}">{{prop}}</a>
        </td>
        <td>
          <ul>
            {% for value in values%}
            <li>
              {% if value.uri %}
              <a class="uri" href="{{value.uri}}" title="{{value.uri}}">{{value.label}}</a>
              {% else %}
              {% if value.literal %}
              <span class="literal">
                {% if value.language %}
                <span xml:lang="{{value.languaje}}">{{value.literal}}</span> <small>({{value.language}})</small>
                {% else %}
                {{value.literal}}
                {% endif %}
              </span>
              {% else %}
              {{value}}
              {% endif %}
              {% endif %}
            </li>
            {% endfor %}
          </ul>
        </td>
      </tr>
      {% endfor %}
    </table>


  </body>

</html>

