JSON Tagger
===========

spaCy finds detailed **Part-of-speech tags** (Noun, Verb, ...) in **Swedish sentences**. This code makes spaCy's Swedish pipeline available via a JSON API.

Play with it at: https://json-tagger.com

## How to run JSON Tagger locally

JSON-Tagger requires Python 3.

1. Clone this project from GitHub:

```
git clone https://github.com/EmilStenstrom/json-tagger.git json-tagger
```

2. Install dependencies:

```
cd json-tagger
pip install -r requirements.txt
```

3. Start the local web server

```
python run.py --run
```

4. Open http://localhost:8000 in your browser. `run.py` permits HTTP for local
   development; normal production startup requires HTTPS. Changes to the
   start-page template are reflected without restarting the server.

The Swedish model runs locally, so tagging does not depend on an external API.

Run the tests
-------------

The trickiest part of delivering an API like JSON Tagger is to handle encodings. I've found that the easiest way to make sure I don't mess them up is to run code that accesses the API from different languages. To run some simple integration tests against a version running locally:

1. Install dependencies

The scripts assume you are running them inside a virtualenv with `python` pointing to Python 3, and that `python2` and `curl` is available on the PATH.

```
pip2 install requests
pip install requests
gem install http
npm install -g request
```

2. Run all the tests

```
tests/run_all
```

If any of the tests fail it will output the difference in output between the result and the expected result.
