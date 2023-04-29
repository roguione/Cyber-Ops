#!/usr/bin/env python3

# Script for automating the setup of FreePBX and Asterisk

import os
import subprocess

# Check if FreePBX is already installed
result = subprocess.run(["which", "fwconsole"], capture_output=True)
if result.returncode == 0:
    fpbx_installed = True
else:
    fpbx_installed = False

# Define variables
extension = "1000"            #Change to proper extension!!!!!
name = "John Doe"             #Change to proper user name!!!!!
secret = "123456"             #Change to proper secret!!!!!

while True:
    # Prompt user for choice
    install_fpbx = input("Do you want to install FreePBX (y/n)? ")
    if install_fpbx.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'.")
        continue

    # Prompt for .csv file paths add more as needed
    cdr_csv = input("Enter path to CDR .csv file: ")
    extensions_csv = input("Enter path to Extensions .csv file: ")
    trunks_csv = input("Enter path to Trunks .csv file: ")
    time_conditions_csv = input("Enter path to Time Conditions .csv file (or press Enter to skip): ")
    ivr_csv = input("Enter path to IVR .csv file (or press Enter to skip): ")
    queues_csv = input("Enter path to Queues .csv file (or press Enter to skip): ")

    # Check if files exist add more as needed 
    if not os.path.isfile(cdr_csv):
        print(f"{cdr_csv} not found.")
        continue
    if not os.path.isfile(extensions_csv):
        print(f"{extensions_csv} not found.")
        continue
    if not os.path.isfile(trunks_csv):
        print(f"{trunks_csv} not found.")
        continue

    # Install dependencies
    print("Installing dependencies...")
    result = subprocess.run(["apt", "update"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    result = subprocess.run(["apt", "install", "-y", "apache2", "mariadb-server", "mariadb-client", "libapache2-mod-php",
                    "php", "php-mysql", "php-cli", "php-curl", "php-gd", "php-pear", "php-xml", "php-mbstring",
                    "curl", "libnewt-dev", "libsqlite3-dev", "libssl-dev", "libxml2-dev"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")

     # Download and install FreePBX if requested and not installed
    if install_fpbx.lower() == 'y' and not fpbx_installed:
        print("Downloading and installing FreePBX...")
        result = subprocess.run(["cd", "/usr/src"], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
        result = subprocess.run(["wget", "http://mirror.freepbx.org/modules/packages/freepbx/freepbx-15.0-latest.tgz"], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
        result = subprocess.run(["tar", "xvfz", "freepbx-15.0-latest.tgz"], capture_output=True, cwd="/usr/src")
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
        result = subprocess.run(["cd", "freepbx-15.0"], capture_output=True, cwd="/usr/src")
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
        result = subprocess.run(["./install"], capture_output=True, cwd="/usr/src/freepbx-15.0")
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    print("FreePBX installed successfully.")
    
    # Configure FreePBX firewall
    print("Configuring FreePBX firewall...")
    result = subprocess.run(["fwconsole", "firewall", "stop"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    result = subprocess.run(["fwconsole", "firewall", "start"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    print("FreePBX firewall configured.")

    # Configure the new extension in FreePBX
    print("Configuring the new extension in FreePBX...")
    fpbx_conf_file = "/etc/asterisk/extensions_custom.conf"
    with open(fpbx_conf_file, "a") as f:
        f.write(f"\n[{extension}]\n")
        f.write(f"username={name}\n")
        f.write(f"secret={secret}\n")
        f.write(f"type=friend\n")
        f.write(f"context=from-internal\n")
        f.write(f"host=dynamic\n")
        f.write(f"disallow=all\n")
        f.write(f"allow=ulaw\n")
        f.write(f"allow=alaw\n")
    result = subprocess.run(["sudo", "fwconsole", "reload"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    print("Extension configured successfully in FreePBX.")

    # Configure a SIP trunk for outbound calls
    print("Configuring a SIP trunk for outbound calls...")
    sip_conf_file = "/etc/asterisk/sip.conf"
    with open(sip_conf_file, "a") as f:
        f.write("\n[outbound-trunk]\n")
        f.write(f"type=peer\n")
        f.write(f"username=YOUR_USERNAME\n")        #Change to proper user name!!!!!
        f.write(f"secret=YOUR_PASSWORD\n")          #Change to proper user Password!!!!!
        f.write(f"host=YOUR_SIP_PROVIDER\n")        #Change to proper SIP_Provider!!!!!
        f.write(f"fromuser=YOUR_PHONE_NUMBER\n")    #Change to proper phone number!!!!!
        f.write(f"trustrpid=yes\n")
        f.write(f"sendrpid=yes\n")
        f.write(f"canreinvite=no\n")
        f.write(f"context=from-internal\n")
    result = subprocess.run(["sudo", "asterisk", "-rx", "sip reload"], capture_output=True)
    if result.returncode != 0:
    raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    print("SIP trunk configured successfully.")

    # Configure an outbound route for the new extension
    print("Configuring an outbound route for the new extension...")
    fpbx_conf_file = "/etc/asterisk/extensions_custom.conf"
    with open(fpbx_conf_file, "a") as f:
        f.write(f"\n[outbound-{extension}]\n")
        f.write(f"include=outbound-trunk\n")
        f.write(f"exten=_X.,1,Set(CALLERID(all)={name} <{extension}>)\n")
        f.write(f"exten=_X.,n,Dial(SIP/${{EXTEN}}@outbound-trunk)\n")
    
    # Restore configuration files
    print("Restoring configuration files...")
    result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asteriskcdrdb", "<", cdr_csv], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asterisk", "<", extensions_csv], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asterisk", "<", trunks_csv], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    if time_conditions_csv:
        result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asterisk", "<", time_conditions_csv], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    if ivr_csv:
        result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asterisk", "<", ivr_csv], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")
    if queues_csv:
        result = subprocess.run(["mysql", "-u", "root", "-p" + db_root_password, "asterisk", "<", queues_csv], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().strip()}")

    # Restart Asterisk service
    print("Restarting Asterisk service...")
    result = subprocess.run(["systemctl", "restart", "asterisk"], capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {result.stderr.decode().strip()}")

    print("Setup complete.")

    try:
        pass

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        continue

except Exception as e:
    print(e)
    break

