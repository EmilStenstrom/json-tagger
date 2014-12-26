from collections import OrderedDict
from server import prepare_data, query_server
from parser import parse_response
from bottle import route, request, run, view

import bottle
bottle.TEMPLATE_PATH = ["api/views/"]
bottle.debug(True)
bottle.TEMPLATES.clear()

@route('/api/')
@view('index')
def index():
    site = "%s://%s" % (request.urlparts.scheme, request.urlparts.netloc)
    return {"site": site}

@route('/api/tag', method=["get", "post"])
def tag():
    data = request.POST.get("data", None)

    if not data:
        data = request.body.getvalue()

    if not data:
        return {"error": "No data posted"}

    data = prepare_data(data)
    response = query_server(data)
    sentences, entities = parse_response(response)

    return OrderedDict([
        ("sentences", sentences),
        ("entities", entities),
    ])

run(host='localhost', port=8000, reloader=True)