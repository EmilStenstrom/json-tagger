from falcon.util.uri import parse_query_string
import json
from api.actions import pos_tagging

class ApiResource(object):
    def parse_request_data(self, raw_post_data):
        encoded_raw_post_data = ""
        try:
            encoded_raw_post_data = str(raw_post_data, 'utf-8')
        except UnicodeDecodeError:
            try:
                encoded_raw_post_data = str(raw_post_data, 'latin-1')
            except UnicodeDecodeError:
                pass

        return encoded_raw_post_data

    def on_post(self, request, response):
        body = request.stream.read()
        encoded_raw_post_data = self.parse_request_data(body)

        pretty = request.get_param("pretty")
        if not pretty:
            pretty = parse_query_string(encoded_raw_post_data).get("pretty", False)

        data = request.get_param("data")
        if not data:
            data = parse_query_string(encoded_raw_post_data).get("data", False)
            if not data:
                data = encoded_raw_post_data

        if not data:
            return {"error": "No data posted or data incorrectly encoded"}

        tagged_json = pos_tagging(data)

        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(tagged_json, **json_kwargs)
