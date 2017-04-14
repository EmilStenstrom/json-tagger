from falcon.util.uri import parse_query_string
import json
from api.actions import pos_tagging

class ApiResource(object):
    def _parse_post_data(self, raw_post_data):
        data_dict = {}

        try:
            body = raw_post_data.decode('ascii')
        except UnicodeDecodeError:
            try:
                body = raw_post_data.decode('utf-8')
            except UnicodeDecodeError:
                body = None

        if body:
            data_dict = parse_query_string(body)

        return data_dict

    def on_post(self, request, response):
        body = request.stream.read()

        # Support posting data via forms
        post_data = self._parse_post_data(body)
        data = post_data.get("data", None)

        # Support posting data via POST body
        if not data:
            data = str(body, "utf-8")

        if not data:
            return {"error": "No data posted"}

        tagged_json = pos_tagging(data)

        pretty = request.get_param("pretty", False)
        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(tagged_json, **json_kwargs)
