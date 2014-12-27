from bottle import route, request, response, run, view
from collections import OrderedDict
from parser import parse_response
from server import query_server
import bottle
import json
import os

@route('/api/')
@view('api/views/index')
def index():
    site = "%s://%s" % (request.urlparts.scheme, request.urlparts.netloc)
    return {"site": site}

@route('/api/tag', method=["get", "post"])
def tag():
    # Support posting data both via forms and via POST body
    data = request.POST.get("data", request.body.getvalue())

    if not data:
        return {"error": "No data posted"}

    raw_text = query_server(data)
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

if __name__ == "__main__":
    environment = os.environ.get("ENVIRONMENT", None)
    assert environment, "Needs $ENVIRONMENT variable set"
    if environment == "development":
        print "RUNNING IN DEVELOPMENT MODE"
        bottle.debug(True)
        bottle.TEMPLATES.clear()
        run(host='localhost', port=8000, reloader=True)
    elif environment == "production":
        print "RUNNING IN PRODUCTION MODE"
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        assert False, "That's not a valid $ENVIRONMENT"
