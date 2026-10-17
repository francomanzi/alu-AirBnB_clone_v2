#!/usr/bin/python3
"""Full deployment of web_static to web servers."""
from fabric.api import env, put, run, local
from os.path import exists, splitext, basename, getsize
from time import strftime

env.hosts = ["100.58.246.240", "34.205.78.161"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


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


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path: path of the archive to deploy.
    Returns:
        True if all operations succeeded, False otherwise.
    """
    if not exists(archive_path):
        return False
    try:
        file_name = basename(archive_path)
        folder_name = splitext(file_name)[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(folder_name, folder_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(folder_name))
        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.

    Returns:
        True if deployment succeeded, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
