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

def do_deploy(archive_path):
    """
    Function to deploy my web_static
    """
    remote_path = "/tmp"

    # upload the achive to the remote server
    run("mkdir -p {}".format(remore_path))
    put(archive_path, remote_path)

    # create directories and extract the archive
    release_path = "/data/web_static/releases"
    release_folder = "web_static"
    
    run ("mkdir -p {}/{}".format(release_path, release_folder))
    run("tar -xvzf {}/{} -C {}/{}".format(
        remote_path,
        archive_path.split("/")[-1],
        release_path,
        release_folder
    ))
    # cleanup
    current_path = "/data/web_static/current"
    run("rm -rf {}".format(current_path))i
    run("rm {}/{}".format(remote_path, archive_path.split("/")[-1]))
    # create symlink
    run("ln -sf {}/{}/ {}".format(release_path, release_folder, current_path))
    print("new version deployed!")



