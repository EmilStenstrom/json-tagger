from fabric.operations import local

def runserver():
    local("java -jar stagger/stagger.jar -modelfile models/swedish.bin -server 127.0.0.1 9000")

def tag(filename):
    local("python stagger/scripts/tagtcp.py 127.0.0.1 9000 %s" % filename)
