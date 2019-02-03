# CS683-Worm Assignment
Write a Internet Worm. <br/>Document the safeguards you used to prevent the widespread release of the worm. <br/>A simple SSH based worm is suggested that uses known passwords to connect to a host is suggested.

## Solution:

### Worm Concept
My worm is called sleepingwormy (just a name). Briefly, it changes the user's account password, then it ssh attack to other machine and find ssh vulnerability, then copies itself and execute on the host machine. Finally it shuts down the current machine. I chose "Change user's password" attack because I wanted the worm to be frightening. When a user logs in and the PC shows wrong password, the user gets scared for couple of seconds. So imagine changing the password and shutting down the machine (in the middle of user's work maybe), then the user is unable to login. "Time is money" so spending time recovering the password costs money (I don't want to sound evil).

### Worm Description
The worm that I created does the following:
1. Attacks the current machine, the attack is basically changing the user account's password. So I am generating a new encrypted password using 'openssl' linux command, then I am runninng 'usermod -p newpass username' that changes the user's password. But I am running it as 'sudo' command by typing echo userpasswrd|sudo -S mycommand. This will allow the python script to run the change password command as 'sudo' without prompting the user to enter a password. Because whenever you type 'sudo' before a command, linux prompts the user to enter the password, so this way the script will fully run without having user interaction.
2. Generates a range of IPs and adds them to a list to be used in the SSH attacks. The range of IPs is static and given by me from 192.168.137.2 - 192.168.137.254.
3. Starts SSH attacks on the IP list generated in step 2 by trying a list of usernames and passwords (static usernames and passwords written by me). SSH attacks are done using a python library called paramiko. When the ssh attack succeeds and the script can access the host machine, the script copies itself to the host machine and excutes there as well, then closes the ssh connection. Then goes back to the SSH attack function to attack a new machine and copy itself to it.
4. When the script finishes the SSH attack, it shuts down the current machine so that the user would spend time figuring out what happened and why s/he can't log in.

### Worm Weaknesses
My worm has some weaknesses like:
1. I am preventing the script to harm my machine so I added an argument to the script so when I run 'python sleepingwormy.py 1' the script will attack the current machine then starts SSH attacks. But that is not correct but I have to do it like this to prevent my laptop from getting attacked. **The weakness is linking the machine attack to an argument
2. Using static IP range instead of writing a code that checks all the IPs in a local network. But what prevented me from doing this is being caught by the Universities network and get expelled. So I am running the SSH attacks on a very small range to be in the safe side.
3. list of usernames and passwords is very limited and small but also I didn't want to make it bigger because each SSH attack on each IP will try the whole list. So I don't want to increase the number of SSH attacks on each IP so that I don't get caught and expelled. 
4. using external library "paramiko" in the script which makes the worm only work on the machine having "paramiko" installed on them.

### 
