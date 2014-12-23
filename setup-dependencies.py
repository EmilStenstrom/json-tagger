import bz2
import os
import tarfile
import urllib

def get_and_unzip_stagger():
    URL = "http://mumin.ling.su.se/projects/stagger/snapshot.tar.bz2"

    if os.path.exists("stagger"):
        print "Stagger already installed, skipping"
        return

    filename = URL.split("/")[-1]
    if not os.path.isfile(filename):
        print "Downloading Stagger from %s" % URL
        urllib.urlretrieve(URL, filename)
    else:
        print "Found existing file, skipping download"

    with tarfile.open(filename) as compfile:
        compfile.extractall()

    os.remove(filename)

def get_and_unzip_models():
    URL = "http://mumin.ling.su.se/projects/stagger/swedish.bin.bz2"

    if os.path.exists("models"):
        print "Models already installed, skipping"
        return

    filename = URL.split("/")[-1]
    if not os.path.isfile(filename):
        print "Downloading models from %s" % URL
        urllib.urlretrieve(URL, filename)
    else:
        print "Found existing file, skipping download"

    with open(filename, "rb") as infile:
        data = bz2.decompress(infile.read())

    os.mkdir("models")
    outpath = "models/" + filename.replace(".bz2", "")
    with open(outpath, "wb") as outfile:
        outfile.write(data)

    os.remove(filename)

get_and_unzip_stagger()
get_and_unzip_models()
