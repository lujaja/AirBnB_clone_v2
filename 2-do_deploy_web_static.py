#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to web servers, using the function do_deploy
"""
from fabric.api import run, put, env, local

env.hosts = [
        "18.207.141.60",
        "52.91.154.167"
    ]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"

def do_deploy(archive_path):
    """
    Function to deploy my web_static
    """
    remote_path = "/tmp"

    # upload the achive to the remote server
    run("mkdir -p /tmp")
    put(archive_path, remote_path)

    # create directories and extract the archive
    release_path = "/data/web_static/releases/"
    current_path = ""
    # timestamp = run(date "+%Y%m%d%H%M%S")
    run ("mkdir -p {}".format(release_path))
    run("tar -xvzf /tmp/web_static_20240203004953.tgz {}/web_static".fomart(
        release_path))
    # cleanup
    run("rm /tmp/web_static_20240203004953.tgz")

    run("mkdir -p /data/web_static/current")
    run("ln -sf /data/web_static/releases/web_static /data/web_static/current")



