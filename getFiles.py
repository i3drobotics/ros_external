#!/usr/bin/python3.6

import subprocess
import os
import shutil

start_dir = os.getcwd()

def get_list_from_stdout(stdout):
    stdout_b = stdout.split()
    stdout_list = []
    for s in stdout_b:
        stdout_list.append(s.decode("utf-8"))
    return stdout_list

def run_command(cmd):
    out = subprocess.Popen(cmd, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT, shell=True)
    stdout,stderr = out.communicate()
    return stdout,stderr

def copy_files(src,dst):
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src,dst)
    else:
        print("Source directory not found")

def copy_packge_files(dest,ros_type="msg"):
    cmd = None
    rosfindmsgs='rosmsg packages'
    rosfindsrvs='rossrv packages'
    if ros_type == "msg":
        cmd = rosfindmsgs
    elif ros_type == "srv":
        cmd = rosfindsrvs
    else:
        print("Invalid type. Must be 'msg' or 'srv'")
        return False
    stdout,stderr = run_command(cmd)
    package_names = get_list_from_stdout(stdout)
    for package_name in package_names:
        print(package_name)
        rosfindpackage='rospack find {}'.format(package_name)
        stdout,stderr = run_command(rosfindpackage)
        full_package_folder = get_list_from_stdout(stdout)[0]
        msg_folder = os.path.join(full_package_folder,ros_type)
        dest_folder = os.path.join(dest,package_name+"/")
        print(dest_folder)
        copy_files(msg_folder,dest_folder)
    return True

rosws = "/home/i3dr/i3dr_mapping"

rosetup="source /opt/ros/kinetic/setup.bash"
rosource="source devel/setup.sh"

m_msg_folder = os.path.join(os.getcwd(),"msgs")
m_srvs_folder = os.path.join(os.getcwd(),"srvs")

copy_packge_files(m_msg_folder,"msg")
copy_packge_files(m_srvs_folder,"srv")