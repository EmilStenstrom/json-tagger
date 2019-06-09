from string import Template

doc_template = Template(open("api/views/index.html", "r").read())

class DocsResource(object):
    def on_get(self, request, response):
        response.set_header("Strict-Transport-Security", "max-age=31536000")
        response.content_type = "text/html"
        response.body = doc_template.substitute(
            site="%s://%s" % (request.scheme, request.headers["HOST"])
        )
