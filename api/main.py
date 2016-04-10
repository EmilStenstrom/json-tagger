import json
from collections import OrderedDict

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
        suc_tags = tagger.tag(weights, sentence)
        annotated_sentence = tuple(zip(sentence, suc_tags))

        sentence_data = []
        for i, (word, annotation) in enumerate(annotated_sentence):
            lemma = lemmatizer.predict(word, annotation)
            suc_pos_tag = annotation.split("|")[0]
            suc_features = "|".join(annotation.split("|")[1:]) or None

            token_data = OrderedDict([
                ("word_index", str(i + 1)),
                ("word_form", word),
                ("lemma", lemma),
                ("suc_tags", OrderedDict([
                    ("pos_tag", suc_pos_tag),
                    ("features", suc_features),
                ])),
                ("token_id", "tok:{j}:{i}".format(j=j, i=i)),
            ])
            sentence_data.append(token_data)

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
