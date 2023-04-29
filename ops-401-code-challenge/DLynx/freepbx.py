#!/usr/bin/env python3

# Script for automating the setup of FreePBX and Asterisk

import os
import subprocess

while True:
    try:
        # Prompt user for choice
        install_fpbx = input("Do you want to install FreePBX (y/n)? ")

        # Prompt for .csv file paths
        cdr_csv = input("Enter path to CDR .csv file: ")
        extensions_csv = input("Enter path to Extensions .csv file: ")
        trunks_csv = input("Enter path to Trunks .csv file: ")

        # Check if files exist
        if not os.path.isfile(cdr_csv):
            raise FileNotFoundError(cdr_csv)
        if not os.path.isfile(extensions_csv):
            raise FileNotFoundError(extensions_csv)
        if not os.path.isfile(trunks_csv):
            raise FileNotFoundError(trunks_csv)

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

        if install_fpbx.lower() == 'y':
            # Download and install FreePBX
            print("Downloading and installing FreePBX...")
            result = subprocess.run(["cd", "/usr/src"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")
            result = subprocess.run(["wget", "http://mirror.freepbx.org/modules/packages/freepbx/freepbx-15.0-latest.tgz"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")
            result = subprocess.run(["tar", "xvfz", "freepbx-15.0-latest.tgz"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")
            result = subprocess.run(["cd", "freepbx"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")
            result = subprocess.run(["./start_asterisk", "start"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")
            result = subprocess.run(["./install", "-n"], capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error running command: {result.stderr.decode().strip()}")

        # Import CDR .csv file
        print("Importing CDR .csv file...")
        result = subprocess.run(["fwconsole", "cdr", "import", cdr_csv], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr.decode().
