# -*- coding: utf-8 -*-
import os
from fabric.api import env, local, settings, abort, run, cd
from fabric.operations import local, put, sudo, get
from fabric.context_managers import prefix
from environment import *

def locale():
    """
        Make locale files download from the server
    """
    with cd(env.rootpath):
        get('locale/*', '../bireme/locale')
 
def reset_db(app):
    """
        Realiza reset do app
    """    
    with prefix('. %s/bin/activate' % env.virtualenv):
        with cd(env.rootpath):   
            run('python manage.py reset %s' % app) 
            run('python manage.py syncdb')
            run('python manage.py loaddata fixtures/%s.json' % app)    

def requirements():
    """
        Install the requirements
    """
    with cd(env.gitpath):
        with prefix('. %s/bin/activate' % env.virtualenv):
            run('pip install -r requirements.txt')

def fixtures(app=None):
    """
        Make new fixtures in server and download it
    """
    if app:
        with prefix('. %s/bin/activate' % env.virtualenv):
            with cd(env.rootpath):
                run('python manage.py dumpdata %s --indent=2 > /tmp/%s.json' % (app, app))
        get('/tmp/%s.json' % app, '../bireme/fixtures')

    else:
        with prefix('. %s/bin/activate' % env.virtualenv):
            with cd(env.rootpath):
                run('python manage.py dumpdata --indent=2 > /tmp/submission.json')
        get('/tmp/submission.json', '../bireme/fixtures')

def migrate():
    """
        Realiza migration local
    """    
    with cd(env.path):
        with prefix('. %s/bin/activate' % env.virtualenv):
            run('python manage.py migrate')

def compilemessages():
    """
        Compile translations from server
    """
    with prefix('. %s/bin/activate' % env.virtualenv):
        with cd(env.rootpath):
            run('python manage.py compilemessages')
    restart_app()

def restart_app():
    """
        Restarts remote wsgi.
    """
    with cd(os.path.join(env.path,'..')):
        run("touch application.wsgi")

def update_version_file():
    with cd(env.rootpath):
        run("git describe --tags | cut -f 1,2 -d - > templates/version.txt")
        # traz o arquivo gerado da versão para minha máquina, e implementa a versão localmente
        get("templates/version.txt", "../bireme/templates")

def update():
    """
        Somente atualiza código (git pull) e restart serviço
    """
    with cd(env.gitpath):
        run("git pull")

    update_version_file()
    restart_app()

def full_update():
    """
        Install requirements, update source and make migrations and update 
    """
    update()
    requirements()
    migrate()

def tag(tag):
    """
        Checkout a tag in the server
    """
    with cd(env.path):
        run('git checkout %s' % tag)
    
    restart_app()
