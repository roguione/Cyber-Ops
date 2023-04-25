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
subnet = input("Please enter the IP address or subnet to scan (e.g. 192.168.1.0/24): ")

# Create Nmap scanner object
nm = nmap.PortScanner()

# Use Nmap to scan target subnet and identify live hosts
nm.scan(hosts=subnet, arguments='-sn')

# Create a list to store vulnerability scan results
results = []

# Prompt user for password to run the vulnerability scan
password = input("Please enter your password to run the vulnerability scan: ")

# Loop through identified live hosts and run Nmap vulnerability scan
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        print(f"Scanning {host} for vulnerabilities...")
        # Run Nmap vulnerability scan on live host with sudo
        output = os.popen(f"echo {password} | sudo -S nmap -sS -sV -T2 -p- -R --randomize-hosts --min-rate=20 {host} --script vuln").read()
        # Append vulnerability scan results to list
        results.append(f"Results for {host}:\n{output}\n")

# Save results to a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "Desktop", "vulnerability_scan_results.txt"), "w") as f:
    f.writelines(results)
    print("Results saved to vulnerability_scan_results.txt on the desktop.")
