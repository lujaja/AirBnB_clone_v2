#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo, using the
function do_pack
"""


def do_pack():
    """
    Compress the contents of the web_static folder into a .tgz archive.
    Returns the path to the archive if successful, None otherwise.
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Define the archive path and name
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)

        # Compress the contents of the web_static folder
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path

    except Exception as e:
        return None
