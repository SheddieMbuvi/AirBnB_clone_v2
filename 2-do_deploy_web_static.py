#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import *
from fabric.operations import run, put, local
from datetime import datetime as d


env.hosts = ['52.91.135.108', '100.25.223.51']
env.user = 'ubuntu'

def do_pack():
    """ generates a .tgz archive """
    name = "versions/web_static_" + str(d.now().year)
    name += str(d.now().month) + str(d.now().day) + str(d.now().hour)
    name += str(d.now().minute) + str(d.now().second) + ".tgz"
    result = local("mkdir -p versions; tar -cvzf \"%s\" web_static" % name)
    if result.failed:
        return NULL
    else:
        return name

def do_deploy(archive_path):
    """ uploads the archive to servers """
    destination = "/tmp/" + archive_path.split("/")[-1]
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False
    filename = archive_path.split("/")[-1]
    f = filename.split(".")[0]
    directory = "/data/web_static/releases/" + f
    run_res = run("mkdir -p \"%s\"" % directory)
    if run_res.failed:
        return False
    run_res = run("tar -xzf %s -C %s" % (destination, directory))
    if run_res.failed:
        return False
    run_res = run("rm %s" % destination)
    if run_res:
        return False
    web = directory + "/web_static/*"
    run_res = run("mv %s %s" % (web, directory))
    if run_res.failed:
        return False
    web = web[0:-2]
    run_res = run("rm -rf %s" % web)
    if run_res.failed:
        return False
    run_res = run("rm -rf /data/web_static/current")
    if run_res.failed:
        return False
    run_res = run("ln -s %s /data/web_static/current" % directory)
    if run_res.failed:
        return False
    return True
