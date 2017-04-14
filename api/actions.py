from collections import OrderedDict
from api.ud_helper import Parser as UD_Parser
from conllu import parser as conllu_parser

# Preload data into memory for quick access
UD_PARSER = UD_Parser(language="swe")

def pos_tagging(data):
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

    return OrderedDict([
        ("sentences", sentences),
    ])
