import falcon
from api.api_resource import ApiResource
from api.docs_resource import DocsResource

app = falcon.API()
app.add_route('/', DocsResource())
app.add_route('/tag', ApiResource())
