 #!/usr/bin/env python3
 
# Justin H, Geneva, Sierra, and Nick A
# File Encrytption Script

# Import required modules
import os
from cryptography.fernet import Fernet

# Function to generate a Fernet key and write it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Fernet key successfully generated.")

# Function to load the Fernet key from the key file, or generate a new one if it doesn't exist
def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Error: Fernet key file not found. Generating new key...")
        generate_key()
        return load_key()

# Function to encrypt a file using the Fernet key
def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        original_data = file.read()
    f = Fernet(key)
    encrypted_data = f.encrypt(original_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    print(f"File {file_path} has been encrypted.")

# Function to decrypt a file using the Fernet key
def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    print(f"File {file_path} has been decrypted.")

# Main loop
while True:
    # Ask user to choose an action
    choice = input("Would you like to encrypt, decrypt or exit? ").lower()
    if choice not in ["encrypt", "decrypt", "exit"]:
        print("Invalid choice. Please try again.")
        continue

    # Ask user to enter a directory path
    start_directory = input("Please enter the directory path: ")
    if not os.path.isdir(start_directory):
        print("Error: directory not found.")
        continue

    # Load the Fernet key
    key = load_key()

    # Encrypt all files in the starting directory and its subdirectories
    if choice == "encrypt":
        for root, dirs, files in os.walk(start_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                encrypt_file(file_path, key)

    # Exit the program
    if choice == "exit":
        print("Exiting...")
        break

    # Decrypt all files in the starting directory and its subdirectories
    elif choice == "decrypt":
        for root, dirs, files in os.walk(start_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    decrypt_file(file_path, key)
                except ValueError:
                    print(f"Error: file {file_path} cannot be decrypted. It may not have been encrypted with this tool.")
