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

env.roledefs = {
    "TEST": ["devappnode"],
    "STAGING": ["app1.dev.apitrary.net"],
    "PRODUCTION": ["app1.live.apitrary.net", "app3.live.apitrary.net"]
}

# SINGLE STEPS
#
#

def copy_public_ssh_key():
    put('./assets/apitrary-staging-deploy.pub', '/tmp/apitrary-staging-deploy.pub')
    sudo('mv /tmp/apitrary-staging-deploy.pub /root/.ssh/apitrary-staging-deploy.pub '
         '&& chmod 644 /root/.ssh/apitrary-staging-deploy.pub')


def copy_secret_ssh_key():
    put('./assets/apitrary-staging-deploy', '/tmp/apitrary-staging-deploy')
    sudo('mv /tmp/apitrary-staging-deploy /root/.ssh/apitrary-staging-deploy '
         '&& chmod 600 /root/.ssh/apitrary-staging-deploy')


def add_ssh_config():
    put('./assets/ssh_config', '/tmp/ssh_config')
    sudo('cat /tmp/ssh_config >> /root/.ssh/config')


def setup_ssh_key():
    sudo('mkdir -p /root/.ssh')
    execute(copy_public_ssh_key)
    execute(copy_secret_ssh_key)
    execute(add_ssh_config)


def install_dependencies():
    sudo('aptitude install -y protobuf-compiler python-pip git-core libcurl4-openssl-dev '
         'python-dev build-essential supervisor')


def create_pygenapi_user():
    sudo('useradd -c pygenapi -s /usr/sbin/nologin -d /home/genapi -m genapi')


def pip_install_pygenapi():
    sudo('pip install git+ssh://git@github.com/apitrary/pygenapi.git')


def pip_upgrade_pygenapi():
    sudo('pip install --upgrade git+ssh://git@github.com/apitrary/pygenapi.git')


def initial_setup():
    execute(setup_ssh_key)
    execute(install_dependencies)
    execute(create_pygenapi_user)
    execute(pip_install_pygenapi())


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