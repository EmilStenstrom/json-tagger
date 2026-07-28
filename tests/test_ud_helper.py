from unittest import TestCase
from unittest.mock import Mock, patch

from api.ud_helper import Parser, ParserException


class ParserTest(TestCase):
    @patch("api.ud_helper.spacy.load")
    def test_loads_swedish_model_without_unused_components(self, load):
        model = Mock()
        load.return_value = model

        Parser("swe", lazy_load=False)

        load.assert_called_once_with(
            "sv_core_news_md",
            exclude=["ner"],
        )

    @patch("api.ud_helper.spacy.load")
    def test_loads_model_lazily(self, load):
        model = Mock()
        load.return_value = model
        parser = Parser("swe")

        parser.parse("Hej")

        model.assert_called_once_with("Hej")

    def test_rejects_unknown_language(self):
        with self.assertRaisesRegex(ParserException, "Cannot find model"):
            Parser("unknown")
