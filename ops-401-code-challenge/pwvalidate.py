import time
import re 
from pathlib import Path

def load_wordlist(filepath: str) -> set:
    """Loads a wordlist from a file and returns a set of words."""
    with open(filepath) as file:
        return set(line.strip() for line in file)

def is_password_weak(password: str, password_list: set) -> bool:
    """Checks if a password is weak by comparing it to a wordlist."""
    return password in password_list

def is_password_strong(password: str) -> bool:
    """Checks if a password is strong by enforcing length and complexity requirements."""
    length_check = len(password) >= 6
    capital_check = any(char.isupper() for char in password)
    number_check = len(re.findall('\d', password)) >= 2
    symbol_check = re.search('[^a-zA-Z0-9]', password) is not None
    return length_check and capital_check and number_check and symbol_check

def run_mode1():
    """Loads a wordlist from a file and prints each word to the console."""
    filepath = input("Enter the file path of your dictionary: ")
    wordlist = load_wordlist(filepath)
    for word in wordlist:
        time.sleep(1)
        print(word)

def run_mode2():
    """Asks the user for a password and checks if it's in a wordlist."""
    filepath = input("Enter the file path of your dictionary: ")
    password_list = load_wordlist(filepath)
    while True:
        password = input("Please enter your password: ")
        if is_password_weak(password, password_list):
            print("Your password is weak. Please beef it up and try again!")
        else:
            print("Your password is beefy enough!")
            break

def run_mode3():
    """Asks the user for a password and checks if it meets complexity requirements."""
    password = input("Please enter your password: ")
    if is_password_strong(password):
        print("SUCCESS! Password meets beefy requirements.")
    else:
        print("Beefy password requirements NOT met. The following requirements MUST be met:")
        if len(password) < 6:
            print("- Please use at least 6 characters.")
        if not any(char.isupper() for char in password):
            print("- Please use at least 1 capital letter.")
        if len(re.findall('\d', password)) < 2:
            print("- Please use at least 2 numbers.")
        if not re.search('[^a-zA-Z0-9]', password):
            print("- Please use at least 1 symbol.")

# User menu
while True:
    print("Select a mode:")
    print("1. Print a wordlist to the console.")
    print("2. Check if a password is weak.")
    print("3. Check if a password is strong.")
    answer = input("Enter the number of the mode you want to run: ")
    if answer == "1":
        run_mode1()
        break
    elif answer == "2":
        run_mode2()
        break
    elif answer == "3":
        run_mode3()
        break
    else:
        print("Invalid mode selection. Please try again.")

# END
