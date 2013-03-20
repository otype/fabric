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
    "STAGING": ["lbapi1.dev.apitrary.net"],
    "PRODUCTION": ["lbapi1.live.apitrary.net"]
}

# SINGLE STEPS
#
#

def install_dependencies():
    sudo('aptitude install -y protobuf-compiler python-pip git-core libcurl4-openssl-dev '
         'python-dev build-essential supervisor')


def put_supervisor_deployr_config():
    put('./assets/supervisor_deployr.conf', '/tmp/supervisor_deployr.conf')
    sudo('mv /tmp/supervisor_deployr.conf /etc/supervisor/conf.d/supervisor_deployr.conf'
         ' && chmod 644 /etc/supervisor/conf.d/supervisor_deployr.conf'
         ' && chown root:root /etc/supervisor/conf.d/supervisor_deployr.conf')


def put_supervisor_buildr_config():
    put('./assets/supervisor_buildr.conf', '/tmp/supervisor_buildr.conf')
    sudo('mv /tmp/supervisor_buildr.conf /etc/supervisor/conf.d/supervisor_buildr.conf'
         ' && chmod 644 /etc/supervisor/conf.d/supervisor_buildr.conf'
         ' && chown root:root /etc/supervisor/conf.d/supervisor_buildr.conf')


def create_pydeployr_user():
    sudo('useradd -c deployr -s /usr/sbin/nologin -d /home/deployr -m deployr')


def create_pybuildr_user():
    sudo('useradd -c buildr -s /usr/sbin/nologin -d /home/buildr -m buildr')


def pip_install_pytools():
    sudo('pip install git+ssh://git@github.com/apitrary/pytools.git')


def add_and_restart_supervisor_for_deployr():
    sudo('supervisorctl stop deployr ; '
         'supervisorctl remove deployr ; '
         'supervisorctl reread && supervisorctl add deployr')


def add_and_restart_supervisor_for_buildr():
    sudo('supervisorctl stop buildr ; '
         'supervisorctl remove buildr ; '
         'supervisorctl reread && supervisorctl add buildr')


def initial_setup():
    execute(install_dependencies)
    execute(put_supervisor_deployr_config)
    execute(put_supervisor_buildr_config)
    execute(create_pydeployr_user)
    execute(create_pybuildr_user)
    execute(pip_install_pytools)
    execute(add_and_restart_supervisor_for_deployr)
    execute(add_and_restart_supervisor_for_buildr)


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
