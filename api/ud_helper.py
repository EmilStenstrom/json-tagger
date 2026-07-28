import spacy


class Parser:
    MODELS = {
        "swe": "sv_core_news_md",
    }

    def __init__(self, language, lazy_load=True):
        self.language = language
        self.model_name = self.MODELS.get(language)
        self.model = None

        if not self.model_name:
            raise ParserException("Cannot find model for language '%s'" % language)

        if not lazy_load:
            self.model = self.load_model()

    def load_model(self):
        try:
            return spacy.load(self.model_name, exclude=["ner"])
        except OSError as error:
            raise ParserException(
                "Cannot load spaCy model '%s'" % self.model_name
            ) from error

    def parse(self, text):
        if not self.model:
            self.model = self.load_model()

        return self.model(text.strip())


class ParserException(Exception):
    pass
