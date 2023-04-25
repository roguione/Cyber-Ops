#!/usr/bin/env python3

# Nmap mapping/vulnerability Stealth scan script
# Is called when uptime sensor declares UP for 5 mins
# Saves results to desktop
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
nm.scan(hosts=subnet, arguments='-p- -sT -T4')

# Create a list to store scan and vulnerability scan results
results = []

# Loop through identified live hosts and run quick Nmap vulnerability scan
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        print(f"Scanning {host} for vulnerabilities...")
        # Run Nmap vulnerability scan on live host
        output = os.popen(f"nmap -sV --script vuln {host}").read()
        # Append vulnerability scan results to list
        results.append(f"\nResults for {host}:\n{output}\n")
    else:
        print(f"No live hosts found on {subnet}")

# Save results to a text file on the desktop
if results:
    with open(os.path.join(os.path.expanduser("~"), "Desktop", "scan_results.txt"), "w") as f:
        f.writelines(results)
        print("Results saved to scan_results.txt on the desktop.")
else:
    print("No live hosts found on the network.")
