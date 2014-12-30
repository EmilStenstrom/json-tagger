from bottle import run
# One way to split a Bottle app into several files
from api.main import *  # NOQA
import bottle
import os

if __name__ == "__main__":
    environment = os.environ.get("ENVIRONMENT", None)
    assert environment, "Needs $ENVIRONMENT variable set"
    if environment == "development":
        print "RUNNING IN DEVELOPMENT MODE"
        bottle.debug(True)
        bottle.TEMPLATES.clear()
        run(host='localhost', port=8000, reloader=True)
    elif environment == "production":
        print "RUNNING IN PRODUCTION MODE"
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        assert False, "That's not a valid $ENVIRONMENT"
