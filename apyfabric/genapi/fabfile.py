# -*- coding: utf-8 -*-
"""

    apitrary-fabric

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from fabric.api import sudo
from fabric.operations import  local, require
from fabric.state import env
from fabric.tasks import execute

# Load the global configs
env.use_shell = True
env.use_ssh_config = True


# Set host list for genapi deployment
env.roledefs = {
    "DEV": [
        "app1.dev.apitrary.net",
        ],
    "LIVE": [
        "app1.live.apitrary.net",
        "app3.live.apitrary.net",
        ]
}

# Genapi info
genapi = {}
genapi['user'] = 'genapi'
genapi['home_dir'] = '/home/genapi'
genapi['app_name'] = 'pygenapi'
genapi['bitbucket'] = {}
genapi['bitbucket']['repo'] = 'git@bitbucket.org:apitrary/pygenapi.git'
genapi['bitbucket']['parent'] = 'origin'
genapi['bitbucket']['branch'] = 'master'


def production():
    env.hosts = [
        "app1.live.apitrary.net",
        "app3.live.apitrary.net"
    ]


def staging():
    env.hosts = ["app1.dev.apitrary.net"]


def pack_up_pygenapi():
    local("cd /tmp; "\
          "rm -rf /tmp/pygenapi; "\
          "rm -f /tmp/pygenapi*; "\
          "git clone {} pygenapi && "\
          "cd /tmp/pygenapi && git archive master | gzip > /tmp/pygenapi.tar.gz".format(genapi['bitbucket']['repo'])
    )


def scp_to_all_hosts():
    for hostname in env.hosts:
        local("scp /tmp/pygenapi.tar.gz {}:/tmp/pygenapi.tar.gz".format(hostname))


def extract_to_app_dir():
    sudo("cd /tmp/pygenapi && tar xvzf /tmp/pygenapi.tar.gz")


def setup_py_install():
    sudo("cd /tmp/pygenapi && python setup.py install")


def setup():
    "Create all base directories"
    require('hosts', provided_by=[production, staging])


def deploy():
    "Deploy genapi"
    require('hosts', provided_by=[production, staging])
    execute(pack_up_pygenapi)
    execute(scp_to_all_hosts)
    execute(extract_to_app_dir)
    execute(setup_py_install)

