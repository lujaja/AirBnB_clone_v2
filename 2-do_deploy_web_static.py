#!/usr/bin/python3
"""
    do_deploy
"""
from fabric.api import run, put, env, sudo

env.hosts = [
    "18.207.141.60",
    "52.91.154.167"
]

def do_deploy(archive_path):
    """
    Function to deploy my web_static
    """
    remote_path = "/tmp"

    # Upload the archive to the remote server
    sudo("mkdir -p {}".format(remote_path))
    put(archive_path, remote_path)

    # Create directories and extract the archive
    release_path = "/data/web_static/releases"
    release_folder = "web_static"

    sudo("mkdir -p {}/{}".format(release_path, release_folder))
    sudo("tar -xvzf {}/{} -C {}/{}".format(remote_path, archive_path.split("/")[-1], release_path, release_folder))

    # Cleanup
    sudo("rm {}/{}".format(remote_path, archive_path.split("/")[-1]))

    # Create symbolic link
    current_path = "/data/web_static/current"
    sudo("rm -rf {}".format(current_path))
    sudo("ln -s {}/{}/ {}".format(release_path, release_folder, current_path))

    print("New version deployed!")

