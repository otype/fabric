# -*- coding: utf-8 -*-
"""

    apitrary-fabric

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from fabric.api import sudo
from fabric.operations import   require
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
#noinspection PyDictCreation
deployr = {}
deployr['user'] = 'deployr'
deployr['home_dir'] = '/home/deployr'
deployr['app_name'] = 'deployr'
deployr['bitbucket'] = {}
deployr['bitbucket']['repo'] = 'git@bitbucket.org:apitrary/deployr.git'
deployr['bitbucket']['parent'] = 'origin'
deployr['bitbucket']['branch'] = 'master'


def production():
    env.hosts = [
        "app1.live.apitrary.net",
        "app3.live.apitrary.net"
    ]
    env.config_env = 'live'


def staging():
    env.hosts = ["app1.dev.apitrary.net"]
    env.config_env = 'dev'


def write_config():
    require('config_env', provided_by=[production, staging])
    sudo("deployr.py -w {}".format(env.config_env))


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
    """Deploy deployr"""
    execute(supervisor_all)


def create_config():
    require('hosts', provided_by=[production, staging])
    execute(write_config)