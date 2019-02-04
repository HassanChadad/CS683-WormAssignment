# CS683-Worm Assignment
Write a Internet Worm. <br/>Document the safeguards you used to prevent the widespread release of the worm. <br/>A simple SSH based worm is suggested that uses known passwords to connect to a host is suggested.

## Solution:

### Worm Concept
My worm is called sleepingwormy (just a name hehe). Briefly, it changes the user's account password, then it ssh attack to other machine and find ssh vulnerability, then copies itself and execute on the host machine. Finally it shuts down the current machine if the password change is successful otherwise it run into an infinite loop creating processes using fork. I chose "Change user's password" attack because I wanted the worm to be frightening. When the user logs in and the PC shows "wrong password", the user gets frightened for couple of seconds. So imagine changing the password and shutting down the machine (in the middle of the user's work maybe), then the user is unable to login. "Time is money" so spending time recovering the password costs money (I don't want to sound evil).

### Worm Description
The worm that I created does the following:
1. It attacks the current machine, the attack is basically changing the user account's password. So I am generating a new encrypted password using 'openssl' linux command, then I am runninng 'usermod -p newpass username' that changes the user's password. But I am running it as 'sudo' command by typing 'echo userpasswrd|sudo -S mycommand'. This will allow the python script to run the change password command as 'sudo' without prompting the user to enter his/her current password. Because whenever you type 'sudo' before a command, linux prompts the user to enter the password, so this way the script will fully run without having user interaction.
2. It generates a range of IPs and adds them to a list to be used in the SSH attacks. The range of IPs is static and given by me from 192.168.137.2 - 192.168.137.254.
3. it starts SSH attacks on the IP list generated in step 2 by trying a list of usernames and passwords (static usernames and passwords written by me). SSH attacks are done using a python library called "paramiko". When the SSH attack succeeds and the script can access the new machine, the script copies itself to the new machine and excutes there as well, then closes the SSH connection. Then goes back to the SSH attack function to attack a new machine and to copy itself to it and so on.
4. When the script finishes the SSH attack, it shuts down the current machine so that the user would spend time figuring out what happened and why s/he can't log in. If the password change in step 1 failed then the script will call infinite fork that will infinitely create child processes using fork function to crash the current machine.

### Worm Weaknesses
My worm has some weaknesses like:
1. I am preventing the script to harm my machine so I added an argument to the script so when I run 'python sleepingwormy.py 1' the script will attack the current machine then starts SSH attacks. But that is not correct but I have to do it like this to prevent my laptop from getting attacked. **The weakness is linking the machine attack to an argument
2. Using static IP range instead of writing a code that checks all the IPs in a local network. But what prevented me from doing this is being caught by the Universities network and getting expelled. So I am running the SSH attacks on a very small range to be in the safe side.
3. list of usernames and passwords is very limited and small but also I didn't want to make it bigger because each SSH attack on each IP will try the whole list. So I don't want to increase the number of SSH attacks on each IP so that I don't get caught and expelled. 
4. using external library "paramiko" in the script makes the worm only work on machines having "paramiko" installed on them.
5. The worm doesn't change the password of the machine that ran the script. So if I ran the script, the script won't change my machine's password but will change the password to all the machines it SSH'ed to and changes their passwords. But from the SSH'ed machine, it can SSH back to my machine and change the password.

### What I learned
I learned a lot from this assignment especially that I had to read many articles and watch plenty of youtube videos to know the "worm" concept and how it works. Programming the worm was challenging too because few are those were brave to put part of their code on a blog and it took me good amount of time to gather all the pieces of my code and make sure everything works starting from SSH attacks to copying file through SSH to attacking current machine.<br/>
My worm is very limited and not powerful and I wish to make it more advanced in the future but not as a project because I feel I need to cover more in this course like spyware, firewalls, web hacking...etc
