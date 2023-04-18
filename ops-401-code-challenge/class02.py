import os
import datetime
import time

# Get target IP address from user
target_ip = input("Enter the target IP address: ")

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
    # Print status, timestamp, and destination IP tested
    print(f"{currentTime} Network {status} to {target}")
    # Return the status
    return status

# Set initial success and failure counters to 0
success = 0
failure = 0

# Continuous ping loop
while True:
    # Call ping_target function to ping the target and print status, timestamp, and destination IP
    status = ping_target(target_ip)
    # Increment success or failure counters
    if status == "success":
        success += 1
        failure = 0
    else:
        success = 0
        failure += 1
    # Check if there have been 3 consecutive failures or successes
    if success == 3:
        print(f"{target_ip} is up!")
        break
    elif failure == 3:
        print(f"{target_ip} is down!")
        break
    # Wait for 2 seconds before sending the next packet
    time.sleep(2)

# Print final status message
if success == 3:
    print(f"{target_ip} is up and running!")
else:
    print(f"{target_ip} is down and cannot be reached.")

