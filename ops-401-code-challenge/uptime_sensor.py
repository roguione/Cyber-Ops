# !/usr/bin/env python3

# Jutin H, Sierra, Nick A, and Geneva
# Uptime Sensor
# 04/19/23

import os
import datetime
import time
import smtplib
import subprocess
from getpass import getpass

# Get target IP address from user
target_ip = input("Enter the target IP address: ")

# Ask user for email and password to use for sending notifications
email = input("Enter your email address: ")
password = getpass("Enter your password: ")

# Set up SMTP session
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_session = smtplib.SMTP(smtp_server, smtp_port)
smtp_session.starttls()

# Log in to email account
smtp_session.login(email, password)

# Initialize host status
host_up = True

# Function to ping target address and print status and timestamp
def ping_target(target):
    # Ping the target
    icmp = os.system(f"ping -c 1 {target}")
    
    # Determine whether the ping was successful
    if icmp == 0:
        status = "up"
    else:
        status = "down"
    
    # Get current timestamp
    current_time = datetime.datetime.now()
    
    # Print status, timestamp, and destination IP tested
    print(f"{current_time} Network {status} to {target}")
    
    # Return the status
    return status

# Function to send email alert
def send_alert(status_before, status_after):
    # Get current timestamp
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Set email subject and message
    if status_before == "up" and status_after == "down":
        subject = "Host Down Alert"
        message = f"The host is down! Host status changed from up to down at {current_time}."
    elif status_before == "down" and status_after == "up":
        subject = "Host Up Alert"
        message = f"The host is up! Host status changed from down to up at {current_time}."
    else:
        return # No status change, so no alert needed
    
    # Send email
    smtp_session.sendmail(email, email, f"Subject: {subject}\n\n{message}")

# Set initial success and failure counters to 0
success = 0
failure = 0

# Continuous ping loop
while True:
    # Ping the target and print status, timestamp, and destination IP
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
        print(f"{target_ip} is up!")
        if not host_up:
            send_alert("down", "up")
            host_up = True
        success = 0
        failure = 0
    elif failure == 3:
        print(f"{target_ip} is down!")
        if host_up:
            send_alert("up", "down")
            host_up = False
        success = 0
        failure = 0
    
    # Wait for 5 seconds before sending the next packet
    time.sleep(5)

# Close SMTP session
smtp_session.quit()

