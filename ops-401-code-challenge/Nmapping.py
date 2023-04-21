#!/usr/bin/env python3
# Nmap mapping script
# Is called when uptime sensor declares UP for 5 mins

import os

# Define target subnet
subnet = "192.168.0.0/24"

# Function to scan network and return list of live hosts
def scan_network(subnet):
    # Use nmap to scan the network for live hosts
    cmd = f"nmap -sn {subnet}"
    output = os.popen(cmd).read()
    # Parse the output to extract live hosts
    hosts = []
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            parts = line.split()
            host = parts[4]
            hosts.append(host)
    # Return the list of live hosts
    return hosts

# Call the scan_network function and print the list of live hosts
hosts = scan_network(subnet)
if len(hosts) == 0:
    print("No live hosts found on network")
else:
    print("Live hosts on network:")
    for host in hosts:
        print(host)
