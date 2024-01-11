#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from contents of web_static.
The contents of the web_static folder of AirBnB Clone repo, using func do_pack
"""
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """ generates a .tgz archive from contents of web_static."""
    filename = strftime('%Y%m%d%H%M%S')
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename)

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None
