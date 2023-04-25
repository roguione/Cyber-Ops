import nmap
import os
import getpass

# Prompt user for network to scan and scan type
subnet = input("Enter the subnet to scan (ex. 192.168.1.0/24): ")
print("Choose the type of network scan:")
print("1. Ping scan (-sn)")
print("2. TCP SYN scan (-sS)")
print("3. TCP connect scan (-sT)")
print("4. UDP scan (-sU)")
print("5. Comprehensive scan (-sS -sV -sC)")
scan_type = input("Enter the number of the scan type to use: ")

# Prompt user for vulnerability scan option
print("Would you like to perform a quick vulnerability scan if any hosts are found?")
print("1. Yes")
print("2. No")
vuln_scan_option = input("Enter the number of the option you choose: ")

# Prompt user for sudo password
sudo_pass = getpass.getpass(prompt="Enter sudo password: ")

# Use Nmap to scan target subnet and identify live hosts and open ports
nm = nmap.PortScanner()
if scan_type == "1":
    nm.scan(hosts=subnet, arguments="-sn")
elif scan_type == "2":
    nm.scan(hosts=subnet, arguments="-sS")
elif scan_type == "3":
    nm.scan(hosts=subnet, arguments="-sT")
elif scan_type == "4":
    nm.scan(hosts=subnet, arguments="-sU")
elif scan_type == "5":
    nm.scan(hosts=subnet, arguments="-sS -sV -sC")
else:
    print("Invalid scan type entered. Please enter a number between 1 and 5.")
    exit()

# Create a list to store scan results
results = []

# Iterate through hosts and open ports and append to results list
for host in nm.all_hosts():
    if nm[host].state() == "up":
        print(f"Host {host} is up.")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                if nm[host][proto][port]['state'] == "open":
                    print(f"Port {port} is open.")
                    results.append((host, port))

# Perform quick vulnerability scan if option is selected and at least one host is found
if vuln_scan_option == "1" and results:
    # Install required packages
    os.system(f"echo {sudo_pass} | sudo -S apt-get update")
    os.system(f"echo {sudo_pass} | sudo -S apt-get install -y nmap")
    os.system(f"echo {sudo_pass} | sudo -S apt-get install -y npm")
    os.system(f"echo {sudo_pass} | sudo -S npm install -g retire")
    
    # Iterate through hosts and run vulnerability scan
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            print(f"Scanning {host} for vulnerabilities...")
            os.system(f"echo {sudo_pass} | sudo -S nmap -sV --script=vulners --script-args mincvss=7.0 {host}")
else:
    print("No vulnerabilities found.")

# Save scan results to a text file on desktop
desktop_path = os.path.join(os.path.expanduser("~/Desktop"), "scan_results.txt")
with open(desktop_path, "w") as file:
    for result in results:
        file.write(f"{result[0]}:{result[1]}\n")
print(f"Scan results saved to {desktop_path}")
