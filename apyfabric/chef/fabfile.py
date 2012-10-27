# -*- coding: utf-8 -*-
"""

    apitrary-fabric

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from fabric.api import sudo
from fabric.decorators import roles
from fabric.operations import require
from fabric.state import env
from fabric.tasks import execute

# Load the global configs
env.use_shell = True
env.use_ssh_config = True


# Set host list
env.roledefs = {
    "DEV": [
        "app1.dev.apitrary.net",
        "db1.dev.apitrary.net",
        "lbapi1.dev.apitrary.net",
        "riak1.dev.apitrary.net",
        "rmq1.dev.apitrary.net",
        "web1.dev.apitrary.net"
    ],
    "LIVE": [
        "app1.live.apitrary.net",
        "app3.live.apitrary.net",
        "cache1.live.apitrary.net",
        "chef1.live.apitrary.net",
        "lbapi1.live.apitrary.net",
        #            "monitor1.live.apitrary.net",
        "pgdb1.live.apitrary.net",
        "rmq1.live.apitrary.net",
        "riak1.live.apitrary.net",
        "riak3.live.apitrary.net",
        "riak5.live.apitrary.net",
        #            "web1.live.apitrary.net",
        #            "web2.live.apitrary.net",
        "web3.live.apitrary.net"
    ]
}


def staging():
    env.hosts = env.roledefs['DEV']


def production():
    env.hosts = env.roledefs['LIVE']


def single_chef_client():
    sudo('chef-client')

def chef_client():
    require('hosts', provided_by=[production, staging])
    execute(single_chef_client)