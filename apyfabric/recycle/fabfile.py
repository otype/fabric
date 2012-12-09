# -*- coding: utf-8 -*-
"""

    apitrary-fabric

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import logging
from fabric.api import sudo
from fabric.decorators import roles
from fabric.state import env
from fabric.tasks import execute

# Load the global configs
env.use_shell = True
env.use_ssh_config = True

# Set host list
env.roledefs = {
    "live-rabbitmq" : ["rmq1.live.apitrary.net"],
    "live-app" : ["app1.live.apitrary.net", "app3.live.apitrary.net"],
    "live-web" : ["web3.live.apitrary.net"],
    "live-lbapi" : ["lbapi1.live.apitrary.net"],
    "dev-rabbitmq" : ["rmq1.dev.apitrary.net"],
    "dev-app" : ["app1.dev.apitrary.net"],
    "dev-web" : ["web1.dev.apitrary.net"],
    "dev-lbapi" : ["lbapi1.dev.apitrary.net"]
}

@roles('live-rabbitmq')
def live_rabbit_restart():
    sudo('/etc/init.d/rabbitmq-server restart', pty=False)

@roles('live-web')
def live_nginx_restart():
    sudo('/etc/init.d/nginx stop && sleep 2 && /etc/init.d/nginx start', pty=False)

@roles('live-app')
def live_app_supervisor_restart():
    sudo('supervisorctl restart deployr_deploy')
    sudo('supervisorctl restart trackr')

@roles('live-app')
def live_app_trackr_restart():
    sudo('supervisorctl restart trackr')

@roles('live-web')
def live_web_delayed_job_restart():
    sudo('supervisorctl restart delayed_job')

@roles('live-lbapi')
def live_lb_supervisor_restart():
    sudo('supervisorctl restart deployr_balance')

@roles('dev-rabbitmq')
def dev_rabbit_restart():
    sudo('/etc/init.d/rabbitmq-server restart', pty=False)

@roles('dev-web')
def dev_nginx_restart():
    sudo('/etc/init.d/nginx stop && sleep 2 && /etc/init.d/nginx start', pty=False)

@roles('dev-app')
def dev_app_supervisor_restart():
    sudo('supervisorctl restart deployr_deploy')
    sudo('supervisorctl restart trackr')

@roles('dev-app')
def dev_app_trackr_restart():
    sudo('supervisorctl restart trackr')

@roles('dev-web')
def dev_web_delayed_job_restart():
    sudo('supervisorctl restart delayed_job')

@roles('dev-lbapi')
def dev_lb_supervisor_restart():
    sudo('supervisorctl restart deployr_balance')

def dev_recycle():
    execute(dev_rabbit_restart)
    execute(dev_nginx_restart)
    execute(dev_app_supervisor_restart)
    execute(dev_lb_supervisor_restart)
    execute(dev_app_trackr_restart)

def live_recycle():
    execute(live_rabbit_restart)
    execute(live_nginx_restart)
    execute(live_app_supervisor_restart)
    execute(live_lb_supervisor_restart)
    execute(live_app_trackr_restart)
