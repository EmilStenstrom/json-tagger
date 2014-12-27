from fabric.operations import local

def runtagger():
    local("java -jar stagger/stagger.jar -modelfile models/swedish.bin -server 127.0.0.1 9000")

def runapi():
    local("ENVIRONMENT=development python api/main.py")
