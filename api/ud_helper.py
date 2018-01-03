import re
from ufal.udpipe import Model, Pipeline, ProcessingError

class Parser:
    MODELS = {
        "swe": "data/swedish-ud-2.0-170801.udpipe",
    }

    def __init__(self, language):
        model_path = self.MODELS.get(language, None)
        if not model_path:
            raise ParserException("Cannot find model for language '%s'" % language)

        model = Model.load(model_path)
        if not model:
            raise ParserException("Cannot load model from file '%s'\n" % model_path)

        self.model = model

    def parse(self, text):
        text = text.strip()

        last_character = text.strip()[-1]
        if re.match(r"\w", last_character, flags=re.UNICODE):
            text += "."

        pipeline = Pipeline(
            self.model,
            "tokenize",
            Pipeline.DEFAULT,
            Pipeline.DEFAULT,
            "conllu"
        )
        error = ProcessingError()

        processed = pipeline.process(text, error)
        if error.occurred():
            raise ParserException(error.message)

        return processed

class ParserException(Exception):
    pass
