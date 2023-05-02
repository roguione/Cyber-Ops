#!/usr/bin/env python

from scapy.all import *
import os

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
open_ports = []
closed_ports = []
filtered_ports = []

for port in ports:
    # Construct the packet
    packet = IP(dst=host)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)

    # Check the response flags
    if response:
        if response[TCP].flags == "SA":
            # Port is open
            print(f"Port {port} is open.")
            open_ports.append(port)
            # Send a RST packet to close the connection gracefully
            rst_packet = IP(dst=host)/TCP(dport=port, flags="R")
            send(rst_packet, verbose=0)
        elif response[TCP].flags == "RA":
            # Port is closed
            print(f"Port {port} is closed.")
            closed_ports.append(port)
        else:
            # Port is filtered and silently dropped
            print(f"Port {port} is filtered and silently dropped.")
            filtered_ports.append(port)

# Show scan results
print("Scan complete!")
print(f"Open ports: {open_ports}")
print(f"Closed ports: {closed_ports}")
print(f"Filtered ports: {filtered_ports}")

# Ask if user wants to save results to desktop
save_results = input("Do you want to save the scan results to your desktop? (Y/N): ")
if save_results.upper() == "Y":
    # Save results to a file in the "results" subdirectory of the current working directory
    desktop_path = os.path.join(os.getcwd(), "results")
    os.makedirs(desktop_path, exist_ok=True)  # create directory if it doesn't exist
    filename = input("Enter a filename for the results (without the file extension): ")
    filepath = os.path.join(desktop_path, f"{filename}.txt")
    with open(filepath, "w") as f:
        f.write(f"Open ports: {open_ports}\n")
        f.write(f"Closed ports: {closed_ports}\n")
        f.write(f"Filtered ports: {filtered_ports}\n")
    print(f"Results saved to {filepath}")
else:
    print("Scan results not saved.")
