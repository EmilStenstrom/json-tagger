from fabric.operations import local

def runtagger():
    local("java -jar stagger/stagger.jar -modelfile models/swedish.bin -server 127.0.0.1 9000")

def runapi():
    local("python api/main.py")
