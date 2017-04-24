from falcon.util.uri import parse_query_string
import json
from api.actions import pos_tagging

class ApiResource(object):
    def parse_request_data(self, raw_post_data):
        try:
            raw_correct_encoded = str(raw_post_data, 'utf-8')
        except UnicodeDecodeError:
            raw_correct_encoded = ""

        try:
            raw_incorrectly_encoded = str(raw_post_data, 'latin-1')
        except UnicodeDecodeError:
            raw_incorrectly_encoded = ""

        post_correct = parse_query_string(raw_correct_encoded).get("data", None)
        post_incorrect = parse_query_string(raw_incorrectly_encoded).get("data", None)

        return post_correct or post_incorrect or raw_correct_encoded or raw_incorrectly_encoded

    def on_post(self, request, response):
        body = request.stream.read()
        data = self.parse_request_data(body)

        if not data:
            return {"error": "No data posted or data incorrectly encoded"}

        tagged_json = pos_tagging(data)

        pretty = request.get_param("pretty", False)
        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(tagged_json, **json_kwargs)
