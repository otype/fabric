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


# Set host list for deployr deployment
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
deployr = {}
deployr['user'] = 'deployr'
deployr['home_dir'] = '/home/deployr'
deployr['app_name'] = 'deployr'
deployr['deploy_dir'] = '/opt/deployr'
deployr['bitbucket'] = {}
deployr['bitbucket']['repo'] = 'git@bitbucket.org:apitrary/deployr.git'
deployr['bitbucket']['parent'] = 'origin'
deployr['bitbucket']['branch'] = 'master'


def production():
    env.hosts = [
        "app1.live.apitrary.net",
        "app3.live.apitrary.net"
    ]


def staging():
    env.hosts = ["app1.dev.apitrary.net"]


def create_deployr_dir():
    sudo("mkdir -p {}".format(deployr['deploy_dir']))


def pack_up_deployr():
    local("cd /tmp; "\
          "rm -rf /tmp/deployr; "\
          "rm -f /tmp/deployr*; "\
          "git clone {} deployr && "\
          "cd /tmp/deployr && git archive master | gzip > /tmp/deployr.tar.gz".format(deployr['bitbucket']['repo'])
    )


def scp_to_all_hosts():
    for hostname in env.hosts:
        local("scp /tmp/deployr.tar.gz {}:/tmp/deployr.tar.gz".format(hostname))


def extract_to_app_dir():
    sudo("cd {} && tar xvzf /tmp/deployr.tar.gz".format(deployr['deploy_dir']))


def install_pip_deps():
    sudo("cd {} && pip install -r requirements.txt".format(deployr['deploy_dir']))


def setup():
    "Create all base directories"
    require('hosts', provided_by=[production, staging])
    execute(create_deployr_dir)


def supervisor_stop():
    sudo("supervisorctl stop deployr")

def supervisor_remove():
    sudo("supervisorctl remove deployr")

def supervisor_reread():
    sudo("supervisorctl reread")

def supervisor_add():
    sudo("supervisorctl add deployr")

def supervisor_start():
    sudo("supervisorctl add deployr")

def supervisor_tail():
    sudo("supervisorctl tail deployr")

def supervisor_all():
    execute(supervisor_stop)
    execute(supervisor_remove)
    execute(supervisor_reread)
    execute(supervisor_add)

def deploy():
    "Deploy deployr"
    execute(pack_up_deployr)
    execute(scp_to_all_hosts)
    execute(extract_to_app_dir)
    execute(install_pip_deps)
    execute(supervisor_all)

