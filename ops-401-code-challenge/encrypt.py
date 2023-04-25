#!/usr/bin/env python3


from cryptography.fernet import Fernet
def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    """
    Load the previously generated key
    """
    return open("key.key", "rb").read()
def encrypt_file(file_path, key):
    """
    Encrypts a file given its file path and a key
    """
    with open(file_path, "rb") as file:
        plaintext = file.read()
    f = Fernet(key)
    encrypted = f.encrypt(plaintext)
    with open(file_path, "wb") as file:
        file.write(encrypted)
def decrypt_file(file_path, key):
    """
    Decrypts a file given its file path and a key
    """
    with open(file_path, "rb") as file:
        encrypted = file.read()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    with open(file_path, "wb") as file:
        file.write(decrypted)
def main():
    # Prompt the user to select a mode
    print("Select a mode:")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Encrypt a message")
    print("4. Decrypt a message")
    mode = int(input("Enter mode: "))
    # Load the previously generated key
    key = load_key()
    if mode == 1:
        # Prompt the user to provide a filepath to a target file
        file_path = input("Enter filepath to file to encrypt: ")
        # Encrypt the file
        encrypt_file(file_path, key)
        print("File encrypted successfully!")
    elif mode == 2:
        # Prompt the user to provide a filepath to a target file
        file_path = input("Enter filepath to file to decrypt: ")
        # Decrypt the file
        decrypt_file(file_path, key)
        print("File decrypted successfully!")
    elif mode == 3:
        # Prompt the user to provide a cleartext string
        message = input("Enter message to encrypt: ")
        plaintext = message.encode('utf-8')
        f = Fernet(key)
        encrypted = f.encrypt(plaintext)
        print("The encrypted message is: " + encrypted.decode('utf-8'))
    elif mode == 4:
        # Prompt the user to provide a message to decrypt
        encrypted = input("Enter message to decrypt: ")
        ciphertext = encrypted.encode('utf-8')
        f = Fernet(key)
        decrypted = f.decrypt(ciphertext)
        print("The decrypted message is: " + decrypted.decode('utf-8'))
if __name__ == "__main__":
    main()