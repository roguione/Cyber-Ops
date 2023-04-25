#!/usr/bin/env python3

# Nmap script to scan for live hosts and open ports on a network and save results to a text file
# Note that while using Nmap stealth scan, it may not completely evade detection
# Therefore, it is important to have appropriate authorization
# Follow the legal and ethical guidelines before performing any network scans
# Especially if your network is monitored for suspicious activities

import nmap
import os

# Define target subnet to scan
subnet = input("Enter the subnet to scan (e.g., 192.168.1.0/24): ")

# Create Nmap scanner object
nm = nmap.PortScanner()

# Use Nmap to scan target subnet and identify live hosts and open ports
nm.scan(hosts=subnet, arguments='-p- -sT')

# Create a list to store scan results
results = []

# Loop through identified live hosts and append results to list
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        print(f"Scanning {host} for open ports...")
        # Append host IP address and open ports to results list
        results.append(f"Host: {host}\nOpen Ports: {nm[host]['tcp'].keys()}\n\n")

# Save results to a text file on the desktop
if results:
    with open(os.path.join(os.path.expanduser("~"), "Desktop", "network_scan_results.txt"), "w") as f:
        f.writelines(results)
        print("Results saved to network_scan_results.txt on the desktop.")
else:
    print("No live hosts or open ports found on the network.")
