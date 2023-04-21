#!/usr/bin/env python3
# Nmap mapping/vulnerability scan script
# Is called when uptime sensor declares UP for 5 mins
# Saves results to desktop

import nmap
import os

# Define target subnet to scan
subnet = "192.168.1.0/24"

# Create Nmap scanner object
nm = nmap.PortScanner()

# Use Nmap to scan target subnet and identify live hosts
nm.scan(hosts=subnet, arguments='-sn')

# Create a list to store vulnerability scan results
results = []

# Loop through identified live hosts and run Nmap vulnerability scan
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        print(f"Scanning {host} for vulnerabilities...")
        # Run Nmap vulnerability scan on live host
        output = os.popen(f"nmap -Pn -sV --script vuln {host}").read()
        # Append vulnerability scan results to list
        results.append(f"Results for {host}:\n{output}\n")

# Save results to a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "Desktop", "vulnerability_scan_results.txt"), "w") as f:
    f.writelines(results)
    print("Results saved to vulnerability_scan_results.txt on the desktop.")

