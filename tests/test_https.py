from unittest import IsolatedAsyncioTestCase

from httpx import ASGITransport, AsyncClient

from server import app


class HTTPSTest(IsolatedAsyncioTestCase):
    async def test_redirects_http_to_https(self):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            follow_redirects=False,
        ) as client:
            response = await client.get("http://example.test/")

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "https://example.test/")

    async def test_documentation_uses_https(self):
        async with AsyncClient(
            transport=ASGITransport(app=app),
        ) as client:
            response = await client.get("https://example.test/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("curl https://example.test/tag", response.text)
        self.assertNotIn("http://example.test", response.text)
