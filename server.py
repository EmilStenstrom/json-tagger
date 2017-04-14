import falcon
from api.api_resource import ApiResource
from api.docs_resource import DocsResource
from middleware import RedirectToHTTPS, RedirectToComDomain

app = falcon.API(middleware=[RedirectToHTTPS(), RedirectToComDomain()])
app.add_route('/', DocsResource())
app.add_route('/tag', ApiResource())
