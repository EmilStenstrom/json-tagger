from collections import OrderedDict

from api.ud_helper import Parser as UD_Parser
from conllu import parse as conllu_parse

# Preload data into memory for quick access
UD_PARSER = UD_Parser(language="swe")

class Action:
    def parse(self):
        raise NotImplementedError()

class POSTagging(Action):
    def parse(self, data):
        sentences_raw = UD_PARSER.parse(data)
        sentences_parsed = conllu_parse(sentences_raw)
        sentences = self.to_json(sentences_parsed)

        return OrderedDict([
            ("sentences", sentences),
        ])

    def to_json(self, sentences_parsed):
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

        return sentences

ACTIONS = {
    "pos_tagging": POSTagging,
}
