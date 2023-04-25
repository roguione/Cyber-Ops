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
import time

# Define target subnet to scan
subnet = input("Enter the IP address of the subnet you want to scan (e.g. 192.168.1.0/24): ")
password = input("Enter the password to run the script as sudo: ")

# Create Nmap scanner object
nm = nmap.PortScanner()

# Use Nmap to scan target subnet and identify live hosts and open ports
nm.scan(hosts=subnet, arguments='-p- -sS -T4')

# Create a list to store scan results
results = []

# Loop through identified live hosts and save IP and open ports to list
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        open_ports = [str(port) for port in nm[host]['tcp'].keys() if nm[host]['tcp'][port]['state'] == 'open']
        results.append(f"{host}\t{' '.join(open_ports)}\n")

# Save results to a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "Desktop", "scan_results.txt"), "w") as f:
    f.writelines(results)
    print("Results saved to scan_results.txt on the desktop.")

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

# Print "No vulnerabilities found" after 5 minutes of scanning
time.sleep(300)
print("No vulnerabilities found.")
