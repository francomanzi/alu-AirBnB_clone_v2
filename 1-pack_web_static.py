#!/usr/bin/python3
"""Create a tgz archive of the web_static folder."""
from fabric.api import local
from time import strftime
from os.path import getsize


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static.

    Returns:
        str: archive path if successful, None otherwise.
    """
    date_time = strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date_time)
    try:
        print("Packing web_static to {}".format(file_name))
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        print("{} packed: {} -> {}Bytes".format(
            "web_static", file_name, getsize(file_name)))
        return file_name
    except (Exception, SystemExit):
        return None
