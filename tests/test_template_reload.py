import os
from string import Template
from unittest import TestCase
from unittest.mock import patch

from server import get_doc_template


class TemplateReloadTest(TestCase):
    def test_reloads_template_in_development(self):
        with (
            patch.dict(os.environ, {"JSON_TAGGER_RELOAD_TEMPLATES": "1"}),
            patch("server.open") as open_file,
        ):
            open_file.return_value.read.return_value = "Changed: $site"

            template = get_doc_template()

        self.assertIsInstance(template, Template)
        self.assertEqual(
            template.substitute(site="https://example.test"),
            "Changed: https://example.test",
        )
