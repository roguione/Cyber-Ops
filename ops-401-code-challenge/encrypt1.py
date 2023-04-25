#!/usr/bin/env python3

# Authors: Justin H & Sierra Maldonado
# Contributors: Geneva and Nick A
# File: Encryption and Decryption

from cryptography.fernet import Fernet

# Func generate and write a key to file
def generate_and_write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Func load key from file
def load_key():
    return open("key.key", "rb").read()

# Func encrypt a file given its file path and a key
def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        original_data = file.read()
    f = Fernet(key)
    encrypted_data = f.encrypt(original_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Func decrypt a file given its file path and a key
def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Func encrypt a message given a cleartext string and a key
def encrypt_message(cleartext, key):
    plaintext = cleartext.encode('utf-8')
    f = Fernet(key)
    encrypted = f.encrypt(plaintext)
    print("The encrypted message is:", encrypted.decode('utf-8'))

# Func decrypt a message given an encrypted message string and a key
def decrypt_message(encrypted_message, key):
    ciphertext = encrypted_message.encode('utf-8')
    f = Fernet(key)
    decrypted = f.decrypt(ciphertext)
    print("The decrypted message is:", decrypted.decode('utf-8'))
    
# The if __name__ == "__main__" statement is used,(at bottom)
# Main func to prompt the user to select a mode
# The "main()" function is called to execute the program's logic.
def main():
    generate_and_write_key()
    key = load_key()

    while True:
        print("\nSelect a mode:")      #  ("\n") before the "Select a mode:" blank line before printing the "Select a mode:" prompt
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Encrypt a message")
        print("4. Decrypt a message")
        print("5. Exit")

        mode = int(input("Enter mode: "))

        if mode == 1:
            file_path = input("Enter file path to encrypt: ")
            encrypt_file(file_path, key)
            print("File encrypted successfully!")

        elif mode == 2:
            file_path = input("Enter file path to decrypt: ")
            decrypt_file(file_path, key)
            print("File decrypted successfully!")

        elif mode == 3:
            cleartext = input("Enter message to encrypt: ")
            encrypt_message(cleartext, key)

        elif mode == 4:
            encrypted_message = input("Enter message to decrypt: ")
            decrypt_message(encrypted_message, key)

        elif mode == 5:
            print("Exiting...")
            break

        else:
            print("Invalid mode selected.")

if __name__ == "__main__":
    main()
