#!/usr/bin/env python3
# script establishes a ping heartbeat to target address

# Import libraries
import os
import datetime
import time

# Define target address
target = "8.8.8.8"

# Function to ping target address and print status and timestamp
def ping_target(target):
    # Receive a single ICMP packet
    icmp = os.system("ping -c 1 " + target)
    if icmp == 0:
        status = "success"
    else:
        status = "failed"
    # Get current timestamp
    currentTime = datetime.datetime.now()
    # Print status and timestamp
    print(f"[{status}] {currentTime}")
    # Return the status
    return status

# Continuous ping loop
success = 0
failure = 0
while True:
    # Call ping_target function to ping the target and print status and timestamp
    status = ping_target(target)
    # Increment success or failure counters
    if status == "success":
        success += 1
        failure = 0
    else:
        success = 0
        failure += 1
    # Check if there have been 3 consecutive failures or successes
    if success == 3:
        print(f"{target} is up!")
        break
    elif failure == 3:
        print(f"{target} is down!")
        break
    # Wait for 2 seconds before sending the next packet
    time.sleep(2)

# Print final status message
if success == 3:
    print(f"{target} is up and running!")
else:
    print(f"{target} is down and cannot be reached.")

