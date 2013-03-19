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


def put_supervisor_deployr_config():
    put('./assets/supervisor_deployr.conf', '/tmp/supervisor_deployr.conf')
    sudo('mv /tmp/supervisor_deployr.conf /etc/supervisor/conf.d/supervisor_deployr.conf'
         ' && chmod 644 /etc/supervisor/conf.d/supervisor_deployr.conf'
         ' && chown root:root /etc/supervisor/conf.d/supervisor_deployr.conf')


def pip_install_pydeployr():
    sudo('rm -rf /root/pytools')
    sudo('cd /root'
         ' && git clone git@github.com:apitrary/pytools.git'
         ' && cd /root/pytools/pydeployr'
         ' && pip install -e .'
    )


def create_pydeployr_user():
    sudo('useradd -c deployr -s /usr/sbin/nologin -d /home/deployr -m deployr')


def add_and_restart_supervisor():
    sudo('supervisorctl stop deployr ; '
         'supervisorctl remove deployr ; '
         'supervisorctl reread && supervisorctl add deployr')


def initial_setup():
    execute(install_dependencies)
    execute(put_supervisor_deployr_config)
    execute(pip_install_pydeployr)
    execute(create_pydeployr_user)
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
