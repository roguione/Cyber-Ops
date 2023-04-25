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

# Get target IP address from user input
subnet = input("Enter target IP address (with CIDR notation): ")

# Get password from user input
password = input("Enter password for sudo access: ")

# Get TCP SYN scan time from user input
tcp_syn_scan_time = input("Enter TCP SYN scan time (in seconds): ")

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
        # Run Nmap vulnerability scan on live host with sudo
        output = os.popen(f"echo {password} | sudo -S nmap -sS -sV -T2 -p- -R --randomize-hosts --min-rate=20 --max-retries 1 --max-scan-delay 0 --max-rtt-timeout 150ms --initial-rtt-timeout {tcp_syn_scan_time}s {host} --script vuln").read()
        # Append vulnerability scan results to list
        results.append(f"Results for {host}:\n{output}\n")

# Save results to a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "Desktop", "vulnerability_scan_results.txt"), "w") as f:
    f.writelines(results)
    print("Results saved to vulnerability_scan_results.txt on the desktop.")
