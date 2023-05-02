#!/usr/bin/env python

from scapy.all import *

# Ask for host IP and port range to scan
host = input("Enter the host IP address to scan: ")
ports = []
while not ports:
    port_input = input("Enter the port(s) to scan (comma-separated or range e.g. 80,443 or 1-100): ")
    # Parse port input
    try:
        if "-" in port_input:
            start, end = map(int, port_input.split("-"))
            ports = range(start, end+1)
        else:
            ports = [int(port) for port in port_input.split(",")]
    except ValueError:
        print("Invalid port input. Please try again.")

# Loop through the port range and test each port
for port in ports:
    # Construct the packet
    packet = IP(dst=host)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)

    # Check the response flags
    if response:
        if response[TCP].flags == "SA":
            # Port is open
            print(f"Port {port} is open.")
            # Send a RST packet to close the connection gracefully
            rst_packet = IP(dst=host)/TCP(dport=port, flags="R")
            send(rst_packet, verbose=0)
        elif response[TCP].flags == "RA":
            # Port is closed
            print(f"Port {port} is closed.")
        else:
            # Port is filtered and silently dropped
            print(f"Port {port} is filtered and silently dropped.")
