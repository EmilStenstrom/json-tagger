from falcon.util.uri import parse_query_string
import json
from api.actions import ACTIONS

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

        action_str = request.get_param("action")
        if not action_str:
            action_str = parse_query_string(encoded_raw_post_data).get("action", None)

        if not action_str or action_str not in ACTIONS:
            action_str = "pos_tagging"

        action = ACTIONS[action_str]()
        tagged_json = action.parse(data)

        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(tagged_json, **json_kwargs)
