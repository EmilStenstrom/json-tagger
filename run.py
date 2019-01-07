#!/usr/bin/env python
import os
import argparse

def run():
	os.system("gunicorn server:app --reload --config gunicorn_config.py")

def deploy():
	os.system("git push dokku master")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--deploy', action="store_true", required=False)
	args = parser.parse_args()

	if args.deploy:
	    deploy()
	else:
		run()

if __name__ == '__main__':
	main()
