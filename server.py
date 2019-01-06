import falcon
from api.api_resource import ApiResource
from api.docs_resource import DocsResource
from middleware import RedirectToComDomain

app = falcon.API(middleware=[RedirectToComDomain()])
app.add_route('/', DocsResource())
app.add_route('/tag', ApiResource())
