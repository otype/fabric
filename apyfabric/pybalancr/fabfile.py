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
    "TEST": ["devlbnode"],
    "STAGING": ["lbapi1.dev.apitrary.net"],
    "PRODUCTION": ["lbapi1.live.apitrary.net"]
}

# SINGLE STEPS
#
#

def install_dependencies():
    sudo('aptitude install -y protobuf-compiler python-pip git-core libcurl4-openssl-dev '
         'python-dev build-essential supervisor')


def put_supervisor_balancr_config():
    put('./assets/supervisor_balancr.conf', '/tmp/supervisor_balancr.conf')
    sudo('mv /tmp/supervisor_balancr.conf /etc/supervisor/conf.d/supervisor_balancr.conf'
         ' && chmod 644 /etc/supervisor/conf.d/supervisor_balancr.conf'
         ' && chown root:root /etc/supervisor/conf.d/supervisor_balancr.conf')


def pip_install_pybalancr():
    sudo('pip install git+ssh://git@github.com/apitrary/deployr.git')


def create_pybalancr_user():
    sudo('useradd -c balancr -s /usr/sbin/nologin -d /home/balancr -m balancr')


def add_and_restart_supervisor():
    sudo('supervisorctl stop balancr ; '
         'supervisorctl remove balancr ; '
         'supervisorctl reread && supervisorctl add balancr')


def initial_setup():
    execute(install_dependencies)
    execute(put_supervisor_balancr_config)
    execute(pip_install_pybalancr)
    execute(create_pybalancr_user)
    execute(add_and_restart_supervisor)


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
