import falcon
from falcon.util.uri import parse_query_string
import json
from collections import OrderedDict

from efselab import lemmatize
from efselab import tokenize

# Imports in tagger.py assume taggers are in the same dir
import sys
sys.path.append("efselab")

from efselab.tagger import SucTagger, UDTagger  # NOQA

lemmatizer = lemmatize.SUCLemmatizer()
lemmatizer.load('efselab/suc-saldo.lemmas')

suc_tagger = SucTagger("efselab/suc.bin")
ud_tagger = UDTagger("efselab/suc-ud.bin")

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

        sentence_list = tokenize.build_sentences(data)
        sentences = []
        for j, sentence in enumerate(sentence_list):
            suc_tags = suc_tagger.tag(sentence)
            lemmas = [lemmatizer.predict(word, suc_tags[i]) for i, word in enumerate(sentence)]
            ud_tags = ud_tagger.tag(sentence, lemmas, suc_tags)
            annotated_sentence = tuple(zip(sentence, lemmas, suc_tags, ud_tags))

            sentence_data = []
            for i, (word, lemma, suc_annotation, ud_annotation) in enumerate(annotated_sentence):
                suc_pos_tag = suc_annotation.split("|")[0]
                suc_features = "|".join(suc_annotation.split("|")[1:]) or None
                ud_pos_tag = ud_annotation.split("|")[0]
                ud_features = "|".join(ud_annotation.split("|")[1:]) or None

                token_data = OrderedDict([
                    ("word_form", word),
                    ("lemma", lemma),
                    ("suc_tags", OrderedDict([
                        ("pos_tag", suc_pos_tag),
                        ("features", suc_features),
                    ])),
                    ("ud_tags", OrderedDict([
                        ("pos_tag", ud_pos_tag),
                        ("features", ud_features),
                    ])),
                    ("token_id", "tok:{j}:{i}".format(j=j, i=i)),
                ])
                sentence_data.append(token_data)

            sentences.append(sentence_data)

        response.content_type = "application/json"

        pretty = request.get_param("pretty", False)
        json_kwargs = {"separators": (',', ':')}
        if pretty:
            json_kwargs = {"indent": 4, "separators": (', ', ': ')}

        response.body = json.dumps(OrderedDict([
            ("sentences", sentences),
        ]), **json_kwargs)
