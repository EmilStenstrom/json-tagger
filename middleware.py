import re

import falcon

_FORWARDED_PROTO_RE = re.compile('proto=([A-Za-z]+)')

class RedirectToHTTPS:
    def process_request(self, request, response):
        if request.host in ["localhost", "127.0.0.1"]:
            return

        if request.protocol.lower() == 'https':
            return

        xfp = request.get_header('X-FORWARDED-PROTO')
        if xfp and xfp.lower() == 'https':
            return

        forwarded = request.get_header('FORWARDED')
        if forwarded:
            first, __, __ = forwarded.partition(',')

            match = _FORWARDED_PROTO_RE.search(first)
            if match and match.group(1).lower() == 'https':
                return

        site_https = request.uri.replace("http://", "https://", 1)
        raise falcon.HTTPMovedPermanently(site_https)
