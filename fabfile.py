"""
- git push to github
- git push to server
- check for sqlite file, if not, generate [skip for now]
- restart apache

TODO:
- staging area lol

"""
from __future__ import with_statement
from fabric.api import local, run, cd, abort, env
from fabric.contrib.console import confirm

# Webfaction
env.hosts = ['paimoe.webfactional.com']

def git_push():
    local("git status")
    if confirm("Have you committed?"):
        local("git push origin master")
    else:
        abort("Commit changes bro")
    
def deploy_wf():
    git_push()
    with cd("/home/paimoe/webapps/perthfuel/"):
        run("git stash") # maybe
        run("git pull origin master") # What bout conflicts olol
        run("apache2/bin/restart")
        
def deploy_epio():
    git_push()
    local("epio upload") # totally complicated

