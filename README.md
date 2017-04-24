JSON Tagger
===========

UDPipe finds detailed **Part-of-speech tags** (Noun, Verb, ...) in **Swedish sentences**. This code makes UDPipe available via a JSON API.

Play with it at: http://json-tagger.herokuapp.com/

## How to run JSON Tagger locally

JSON-Tagger is built for Python 3.6. I haven't tested it on other versions, so it might work or other 3.x versions, but not on Python 2.

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

4. Surf to http://localhost:8000 in your browser!
