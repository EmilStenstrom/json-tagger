from bottle import route, request, response, view
from collections import OrderedDict
from api.parser import parse_response
from api.server import query_server
import json

STAGGER_ADDRESS = "mumin.ling.su.se"
STAGGER_PORT = 46502

@route('/')
@view('api/views/index')
def index():
    site = "%s://%s" % (request.urlparts.scheme, request.urlparts.netloc)
    return {"site": site}

@route('/tag', method=["get", "post"])
def tag():
    # Support posting data both via forms and via POST body
    data = request.POST.get("data", request.body.getvalue())

    if not data:
        return {"error": "No data posted"}

    raw_text = query_server(data, STAGGER_ADDRESS, STAGGER_PORT)
    sentences, entities = parse_response(raw_text)

    response.content_type = "application/json"

    pretty = request.POST.get("pretty", False)
    json_kwargs = {"separators": (',', ':')}
    if pretty:
        json_kwargs = {"indent": 4, "separators": (', ', ': ')}

    return json.dumps(OrderedDict([
        ("sentences", sentences),
        ("entities", entities),
    ]), **json_kwargs)
