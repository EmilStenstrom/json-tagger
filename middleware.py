import re

import falcon

_FORWARDED_PROTO_RE = re.compile('proto=([A-Za-z]+)')

class RedirectToComDomain:
    def process_request(self, request, response):
        if request.host != "json-tagger.herokuapp.com":
            return

        site_com = request.uri.replace("json-tagger.herokuapp.com", "json-tagger.com", 1)
        raise falcon.HTTPMovedPermanently(site_com)
