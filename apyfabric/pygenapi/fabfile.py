# -*- coding: utf-8 -*-
"""

    apitrary-fabric

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from fabric.api import sudo
from fabric.decorators import roles
from fabric.operations import put
from fabric.state import env
from fabric.tasks import execute

# GLOBALS
#
#
env.use_shell = True
env.use_ssh_config = True
env.warn_only = True

env.roledefs = {
    "TEST": ["devappnode"],
    "STAGING": ["app1.dev.apitrary.net"],
    "PRODUCTION": ["app1.live.apitrary.net", "app3.live.apitrary.net"]
}

# SINGLE STEPS
#
#

def install_dependencies():
    sudo('aptitude install -y protobuf-compiler python-pip git-core libcurl4-openssl-dev '
         'python-dev build-essential supervisor')


def create_pytrackr_user():
    sudo('useradd -c trackr -s /usr/sbin/nologin -d /home/trackr -m trackr')


def create_pygenapi_user():
    sudo('useradd -c pygenapi -s /usr/sbin/nologin -d /home/genapi -m genapi')


def put_supervisor_trackr_config():
    put('./assets/supervisor_trackr.conf', '/tmp/supervisor_trackr.conf')
    sudo('mv /tmp/supervisor_trackr.conf /etc/supervisor/conf.d/supervisor_trackr.conf'
         ' && chmod 644 /etc/supervisor/conf.d/supervisor_trackr.conf'
         ' && chown root:root /etc/supervisor/conf.d/supervisor_trackr.conf')


def pip_install_pygenapi():
    sudo('pip install git+ssh://git@github.com/apitrary/pygenapi.git')


def pip_upgrade_pygenapi():
    sudo('pip install --upgrade git+ssh://git@github.com/apitrary/pygenapi.git')


def add_and_restart_supervisor_for_trackr():
    sudo('supervisorctl stop trackr ; '
         'supervisorctl remove trackr ; '
         'supervisorctl reread && supervisorctl add trackr')


def initial_setup():
    execute(install_dependencies)
    execute(create_pytrackr_user)
    execute(create_pygenapi_user)
    execute(put_supervisor_trackr_config)
    execute(pip_install_pygenapi)
    execute(add_and_restart_supervisor_for_trackr)


# ROLES-BASED CALLS
#
#

@roles('TEST')
def test_setup():
    execute(initial_setup)


@roles('STAGING')
def staging_setup():
    execute(initial_setup)


@roles('PRODUCTION')
def production_setup():
    execute(initial_setup)


@roles('TEST')
def test_update():
    execute(pip_upgrade_pygenapi)


@roles('STAGING')
def staging_update():
    execute(pip_upgrade_pygenapi)


@roles('PRODUCTION')
def production_update():
    execute(pip_upgrade_pygenapi)