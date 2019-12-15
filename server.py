import json
from string import Template

import typing
from api.actions import ACTIONS
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.formparsers import FormParser

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

doc_template = Template(open("api/views/index.html", "r").read())

@app.get("/", response_class=HTMLResponse)
async def readme(request: Request):
    return doc_template.substitute(
        site="%s://%s" % (request.url.scheme, request.headers["HOST"])
    )

def maybe_pretty_json_response(indent, separators):
    class MyJSONResponse(JSONResponse):
        def render(self, content: typing.Any) -> bytes:
            return json.dumps(
                content,
                ensure_ascii=True,
                allow_nan=False,
                indent=indent,
                separators=separators,
            ).encode("utf-8")
    return MyJSONResponse

@app.post("/tag")
async def tag(
    pretty: bool = False,
    request: Request = None,
):
    data = await request.body()

    async def mock_stream(data):
        yield data
        yield b""

    parser = FormParser(request.headers, mock_stream(data))
    form = await parser.parse()

    data = form.get("data") or str(data, "utf-8")
    action = form.get("action") or "pos_tagging"
    pretty = pretty or form.get("pretty") or False

    if not data:
        return {"error": "No data posted or data incorrectly encoded"}

    action = ACTIONS[action]()
    tagged_json = action.parse(data)

    if pretty:
        return maybe_pretty_json_response(indent=4, separators=(", ", ": "))(tagged_json)

    return maybe_pretty_json_response(indent=None, separators=(",", ":"))(tagged_json)
