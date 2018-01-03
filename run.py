#!/usr/bin/env python
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--run', action="store_true")
parser.add_argument('--deploy', action="store_true")
args = parser.parse_args()

if not any(vars(args).values()):
    parser.print_help()
elif args.run:
    os.system("gunicorn server:app --reload --config gunicorn_config.py")
elif args.deploy:
    os.system("git push heroku master")
