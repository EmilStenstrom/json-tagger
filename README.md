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

3. Get a UDPipe model file

Download the latest version of the udipe models from http://ufal.mff.cuni.cz/udpipe#download. Pick the language you are interested in, and put that file inside the *data* directory. Now update the path to the file in ud_helper, and in actions.py if you use a language other than Swedish.

4. Start the local web server

```
python run.py --run
```

5. Surf to http://localhost:8000 in your browser!

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
