import sys
import os
import argparse
import shutil

from efselab import build

parser = argparse.ArgumentParser()
parser.add_argument('--run', action="store_true")
parser.add_argument('--deploy', action="store_true")
parser.add_argument('--update', action="store_true")
args = parser.parse_args()

if not any(vars(args).values()):
    parser.print_help()
elif args.run:
    os.system("ENVIRONMENT=development python server.py")
elif args.deploy:
    os.system("git push heroku master")
elif args.update:
    if not os.path.exists("../efselab/"):
        sys.exit("Couldn't find a local efselab checkout...")

    shutil.copy("../efselab/fasthash.c", "./efselab")
    shutil.copy("../efselab/lemmatize.c", "./efselab")
    shutil.copy("../efselab/pysuc.c", "./efselab/suc.c")
    shutil.copy("../efselab/tokenize.py", "./efselab/")

    if not os.path.exists("../efselab/swe-pipeline"):
        sys.exit("Couldn't find a local swe-pipeline directory for models...")

    shutil.copy("../efselab/swe-pipeline/suc.bin", "./efselab")
    shutil.copy("../efselab/swe-pipeline/suc-saldo.lemmas", "./efselab")

    print("Building new files...")
    os.chdir("efselab")
    build.main()
