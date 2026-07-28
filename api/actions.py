from collections import OrderedDict

from api.ud_helper import Parser

# Preload data into memory for quick access
PARSER = Parser(language="swe")


class Action:
    def parse(self):
        raise NotImplementedError()

class POSTagging(Action):
    def parse(self, data):
        document = PARSER.parse(data)
        sentences = self.to_json(document)

        return OrderedDict([
            ("sentences", sentences),
        ])

    def to_json(self, document):
        sentences = []
        for j, sentence in enumerate(document.sents):

            sentence_data = []
            for i, token in enumerate(sentence):
                ud_features = token.morph.to_dict() or None

                token_data = OrderedDict([
                    ("word_form", token.text),
                    ("lemma", token.lemma_),
                    ("ud_tags", OrderedDict([
                        ("pos_tag", token.pos_),
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
