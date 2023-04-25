#!/usr/bin/env python3

# Nmap mapping/vulnerability scan script
# Scans the local network for live hosts and open ports, and performs a quick vulnerability scan on each host found
# Saves results to desktop
# Note that while using Nmap stealth scan, it may not completely evade detection
# Therefore, it is important to have appropriate authorization
# Follow the legal and ethical guidelines before performing any network scans
# Especially if your network is monitored for suspicious activities

import nmap
import os
import getpass

# Define target subnet to scan
subnet = input("Enter target subnet to scan (e.g. 192.168.1.0/24): ")

# Create Nmap scanner object
nm = nmap.PortScanner()

# Prompt user to choose from a list of scan options
print("Choose scan type:")
print("1. TCP connect scan (-sT)")
print("2. TCP SYN scan (-sS)")
scan_option = input("Enter option number: ")

# Use Nmap to scan target subnet and identify live hosts and open ports
if scan_option == "1":
    # TCP connect scan
    nm.scan(hosts=subnet, arguments='-sT -Pn')
elif scan_option == "2":
    # TCP SYN scan
    nm.scan(hosts=subnet, arguments='-sS -T4 -Pn')
else:
    print("Invalid option. Exiting.")
    exit()

# Create a list to store scan results
results = []

# Loop through identified live hosts and run quick vulnerability scan
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        print(f"\nScanning {host} for vulnerabilities...")
        # Run Nmap vulnerability scan on live host with sudo
        password = getpass.getpass(prompt="Enter password to run vulnerability scan: ")
        output = os.popen(f"echo {password} | sudo -S nmap -sV --script=vuln {host}").read()
        # Append vulnerability scan results to list
        results.append(f"\nResults for {host}:\n{output}")

# Save results to a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "Desktop", "scan_results.txt"), "w") as f:
    f.writelines(results)
    print("Results saved to scan_results.txt on the desktop.")
