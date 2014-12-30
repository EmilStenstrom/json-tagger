from fabric.operations import local

def run():
    local("ENVIRONMENT=development python api/main.py")

def deploy():
    local("git push heroku master")
