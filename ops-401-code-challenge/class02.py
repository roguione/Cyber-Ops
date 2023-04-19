# !/usr/bin/env python3

# Jutin H, Sierra, Nick A, and Geneva
# Uptime Sensor
# 04/19/23

import smtplib
import datetime
import subprocess
import time
from getpass import getpass

# Ask user for email and password to use for sending notifications
email = input("Enter your email address: ")
password = getpass("Enter your password: ")

# Set up SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()

# Log in to email account
s.login(email, password)

# Initialize host status
host_up = True

# Function to send email alert
def send_alert(status_before, status_after):
    # Get current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Set email message
    if status_before == "up" and status_after == "down":
        subject = "Host Down Alert"
        message = f"The host is down! Host status changed from up to down at {now}."
    elif status_before == "down" and status_after == "up":
        subject = "Host Up Alert"
        message = f"The host is up! Host status changed from down to up at {now}."
    else:
        return # No status change, so no alert needed
    
    # Send email
    s.sendmail(email, email, f"Subject: {subject}\n\n{message}")

# Function to check host status and send email alert if status changes
def check_host():
    # Ping host
    result = subprocess.run(['ping', '-c', '1', 'google.com'], stdout=subprocess.PIPE)
    
    # Check if host is up or down
    if "1 received" in result.stdout.decode('utf-8'):
        current_status = "up"
    else:
        current_status = "down"
    
    # Check if status has changed
    global host_up
    if current_status != host_up:
        send_alert("up" if host_up else "down", current_status)
        host_up = current_status

# Run check_host function in a loop
while True:
    check_host()
    # Wait 1 minute before checking again
    time.sleep(60)

# Close SMTP session
s.quit()
import os
import datetime
import time
import smtplib
import subprocess
from getpass import getpass

# Ask user for email and password to use for sending notifications
email = input("Enter your email address: ")
password = getpass("Enter your password: ")

# Set up SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()

# Log in to email account
s.login(email, password)

# Get target IP address from user
target_ip = input("Enter the target IP address: ")

# Initialize host status
host_up = True

# Function to ping target address and print status and timestamp
def ping_target(target):
    # Receive a single ICMP packet
    icmp = os.system("ping -c 1 " + target)
    if icmp == 0:
        status = "up"
    else:
        status = "down"
    # Get current timestamp
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print status, timestamp, and destination IP tested
    print(f"{currentTime} Network {status} to {target}")
    # Return the status
    return status

# Set initial success and failure counters to 0
success = 0
failure = 0

# Function to send email alert
def send_alert(status_before, status_after):
    # Get current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Set email message
    if status_before == "up" and status_after == "down":
        subject = "Host Down Alert"
        message = f"The host is down! Host status changed from up to down at {now}."
    elif status_before == "down" and status_after == "up":
        subject = "Host Up Alert"
        message = f"The host is up! Host status changed from down to up at {now}."
    else:
        return # No status change, so no alert needed
    
    # Send email
    s.sendmail(email, email, f"Subject: {subject}\n\n{message}")

# Continuous ping loop
while True:
    # Call ping_target function to ping the target and print status, timestamp, and destination IP
    status = ping_target(target_ip)
    # Increment success or failure counters
    if status == "up":
        success += 1
        failure = 0
    else:
        success = 0
        failure += 1
    # Check if there have been 3 consecutive failures or successes
    if success == 3:
        if not host_up:
            send_alert("down", "up")
            host_up = True
        success = 0
        failure = 0
    elif failure == 3:
        if host_up:
            send_alert("up", "down")
            host_up = False
        success = 0
        failure = 0
    # Wait for 2 seconds before sending the next packet
    time.sleep(2)

# Close SMTP session
s.quit()

