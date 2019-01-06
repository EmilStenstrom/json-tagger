import re
from ufal.udpipe import Model, Pipeline, ProcessingError

class Parser:
    MODELS = {
        "swe": "data/swedish-talbanken-ud-2.3-181115.udpipe",
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

        # Adding a period improves detection on especially short sentences
        period_added = False
        last_character = text.strip()[-1]
        if re.match(r"\w", last_character, flags=re.UNICODE):
            text += "."
            period_added = True

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

        # Remove the period to make sure input corresponds to output
        if period_added:
            processed = "\n".join(processed.rstrip().split("\n")[:-1]) + "\n\n"

        return processed

class ParserException(Exception):
    pass
