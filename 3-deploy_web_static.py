#!/usr/bin/python3
"""
Fabric script creates and distributes archive to my web servers.
Uses the function deploy.
execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/school -u ubuntu
"""
import os.path
from datetime import datetime
from fabric.api import *

env.hosts = ['100.25.103.238', '54.160.69.44']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """
    Creates a tar gzipped archive of directory.
    """
    dat = datetime.utcnow()
    file = "version/web_static_{}{}{}{}{}{}.tgz".format(dat.year,
                                                        dat.month,
                                                        dat.day,
                                                        dat.hour,
                                                        dat.minute,
                                                        dat.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
        if local("tar -cvzf {} web_static".format(file)).failed is True:
            return None
        return file


def do_deploy(archive_path):
    """
    It distributes an archive to a web server.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True       


def do_deploy():
    """
    Creates and distributes an archive to a web server.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
