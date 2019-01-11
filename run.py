#!/usr/bin/env python
import os
import argparse

def run():
	""" Reuse the Procfile to start the dev server """
	with open("Procfile", "r") as f:
		command = f.read().strip()

	command = command.replace("web: ", "")
	command = command.replace("--preload", "--reload")
	os.system(command)

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
