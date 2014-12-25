from collections import OrderedDict
from server import prepare_data, query_server
from parser import parse_response
from bottle import route, request, run

@route('/api/')
def index():
    return '''
        <form action="/api/tag" method="post">
            <textarea name="data"></textarea>
            <button type="submit">Tagga</button>
        </form>
    '''

@route('/api/tag', method=["get", "post"])
def tag():
    if not request.POST:
        return {"error": "No data posted"}
    data = prepare_data(request.POST["data"])
    response = query_server(data)
    sentences, entities = parse_response(response)

    return OrderedDict([
        ("sentences", sentences),
        ("entities", entities),
    ])

run(host='localhost', port=8000, reloader=True)
