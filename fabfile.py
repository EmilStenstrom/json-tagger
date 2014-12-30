from fabric.operations import local

def run():
    local("ENVIRONMENT=development python runner.py")

def deploy():
    local("git push heroku master")
