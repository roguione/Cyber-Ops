#!/usr/bin/env python3

# Nmap network scan and quick vulnerability scan script
# Prompts for password to run sudo commands
# Saves results to desktop

import nmap
import os
import getpass

# Prompt for password to run sudo commands
password = getpass.getpass("Enter sudo password: ")

# Define target subnet to scan
subnet = input("Enter target subnet to scan (e.g. 192.168.1.0/24): ")

# Define Nmap scan options
scan_options = input("Enter Nmap scan options (e.g. -sS -T4): ")

# Create Nmap scanner object
nm = nmap.PortScanner()

# Use Nmap to scan target subnet and identify live hosts
print(f"Scanning {subnet} for live hosts...")
nm.scan(hosts=subnet, arguments=scan_options)

# Check if any live hosts were found
live_hosts = nm.all_hosts()
if not live_hosts:
    print("No live hosts found on network.")
else:
    # Save IP addresses of live hosts to a file on the desktop
    with open(os.path.join(os.path.expanduser("~"), "Desktop", "live_hosts.txt"), "w") as f:
        f.writelines([host + "\n" for host in live_hosts])
        print("Live hosts saved to live_hosts.txt on the desktop.")

    # Prompt for quick vulnerability scan
    if input("Do you want to perform a quick vulnerability scan on the live hosts? (y/n): ").lower() == "y":
        # Create a list to store vulnerability scan results
        results = []

        # Loop through identified live hosts and run Nmap vulnerability scan
        for host in live_hosts:
            print(f"Scanning {host} for vulnerabilities...")
            # Run Nmap vulnerability scan on live host with sudo
            output = os.popen(f"echo '{password}' | sudo -S nmap -sS -sV -T2 -p- -R --randomize-hosts --min-rate=20 {host} --script vuln").read()
            # Append vulnerability scan results to list
            results.append(f"Results for {host}:\n{output}\n")

        # Save vulnerability scan results to a file on the desktop
        with open(os.path.join(os.path.expanduser("~"), "Desktop", "vulnerability_scan_results.txt"), "w") as f:
            f.writelines(results)
            print("Vulnerability scan results saved to vulnerability_scan_results.txt on the desktop.")
