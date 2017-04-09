from falcon.util.uri import parse_query_string
import json
from collections import OrderedDict
from api.ud_helper import Parser as UD_Parser
from conllu import parser as conllu_parser

UD_PARSER = UD_Parser(language="swe")

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

        sentences_raw = UD_PARSER.parse(data)
        sentences_parsed = conllu_parser.parse(sentences_raw)

        sentences = []
        for j, sentence_parsed in enumerate(sentences_parsed):

            sentence_data = []
            for i, word_parsed in enumerate(sentence_parsed):
                word = word_parsed.get("form", None)
                lemma = word_parsed.get("lemma", None)
                ud_pos_tag = word_parsed.get("upostag", None)
                ud_features = word_parsed.get("feats")

                token_data = OrderedDict([
                    ("word_form", word),
                    ("lemma", lemma),
                    ("ud_tags", OrderedDict([
                        ("pos_tag", ud_pos_tag),
                        ("features", ud_features),
                    ])),
                    ("sentence_id", j),
                    ("word_id", i),
                ])
                sentence_data.append(token_data)

            sentences.append(sentence_data)

        response.set_header("Strict-Transport-Security", "max-age=31536000")
        response.content_type = "application/json"

        pretty = request.get_param("pretty", False)
        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(OrderedDict([
            ("sentences", sentences),
        ]), **json_kwargs)
