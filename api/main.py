import json
from collections import OrderedDict
from itertools import groupby

from bottle import route, request, response, view

from efselab import suc as tagger
from efselab import lemmatize
from efselab import tokenize

lemmatizer = lemmatize.SUCLemmatizer()
lemmatizer.load('efselab/suc-saldo.lemmas')

@route('/')
@view('api/views/index')
def index():
    site = "%s://%s" % (request.urlparts.scheme, request.urlparts.netloc)
    return {"site": site}

@route('/tag', method=["get", "post"])
def tag():
    # Support posting data via forms
    data = request.POST.data

    # Support posting data via POST body
    if not data:
        data = str(request.body.read(), "utf-8")

    if not data:
        return {"error": "No data posted"}

    weights = None
    with open('efselab/suc.bin', 'rb') as f:
        weights = f.read()

    sentence_list = tokenize.build_sentences(data)
    sentences = []
    entities = []
    for j, sentence in enumerate(sentence_list):
        tags = tagger.tag(weights, sentence)
        tokens_and_tags = tuple(zip(sentence, tags))

        sentence_data = []
        for i, (word, features) in enumerate(tokens_and_tags):
            lemma = lemmatizer.predict(word, features)
            pos_tag = features.split("|")[0]
            morph_feat = "|".join(features.split("|")[1:]) or None

            token_data = OrderedDict([
                ("word_index", str(i + 1)),
                ("word_form", word),
                ("lemma", lemma),
                ("pos_tag", pos_tag),
                ("morph_feat", morph_feat),
                ("token_id", "tok:{j}:{i}".format(j=j, i=i)),
            ])
            sentence_data.append(token_data)

        grouped_tokens = groupby(sentence_data, lambda token: token["pos_tag"])
        for token_group in [list(v) for k, v in grouped_tokens if k == "PM"]:
            entity_data = OrderedDict([
                ("word_form", " ".join([token["word_form"] for token in token_group])),
                ("token_ids", [token["token_id"] for token in token_group]),
            ])
            entities.append(entity_data)

        sentences.append(sentence_data)

    response.content_type = "application/json"

    pretty = request.POST.get("pretty", False)
    json_kwargs = {"separators": (',', ':')}
    if pretty:
        json_kwargs = {"indent": 4, "separators": (', ', ': ')}

    return json.dumps(OrderedDict([
        ("sentences", sentences),
        ("entities", entities),
    ]), **json_kwargs)
