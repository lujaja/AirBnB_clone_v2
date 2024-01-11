#!/usr/bin/python3
"""
Fabric script creates and distributes archive to my web servers.
Uses the function deploy.
"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['100.25.103.238', '54.160.69.44']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
    Uses fabric to distribute archives.
    """
    try:
        if not (path.exists(archive_path)):
            return False
        # Command that uploads the archive
        put(archive_path, '/tmp/')

        # It creates target directory
        time_stamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(time_stamp))

        # It uncompreesses archive and deletes .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'.format(time_stamp, time_stamp))

        # Removes archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(time_stamp))

        # Move Contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(time_stamp, time_stamp))

        # Removes extraneous web_static directory
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'.format(time_stamp))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establishing  symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(time_stamp))
    except Exception as e:
        return False

    # Returns True on success
    return True
