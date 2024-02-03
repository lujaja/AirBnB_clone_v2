#!/usr/bin/python3
"""
    do_deploy
"""
from fabric.api import run, put, env

env.hosts = [
    "18.207.141.60",
    "52.91.154.167"
]

def do_deploy(archive_path):
    """
    Function to deploy my web_static
    """
    run("sudo su")
    remote_path = "/tmp"

    # Upload the archive to the remote server
    run("mkdir -p {}".format(remote_path))
    put(archive_path, remote_path)

    # Create directories and extract the archive
    release_path = "/data/web_static/releases"
    release_folder = "web_static"

    run("mkdir -p {}/{}".format(release_path, release_folder))
    run("tar -xvzf {}/{} -C {}/{}".format(remote_path, archive_path.split("/")[-1], release_path, release_folder))

    # Cleanup
    run("rm {}/{}".format(remote_path, archive_path.split("/")[-1]))

    # Create symbolic link
    current_path = "/data/web_static/current"
    run("rm -rf {}".format(current_path))
    run("ln -s {}/{}/ {}".format(release_path, release_folder, current_path))

    print("New version deployed!")

