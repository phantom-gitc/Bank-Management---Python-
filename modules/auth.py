import sys
from modules.storage import ADMIN_FILE, load_data


# asks for admin username and password with a maximum of 3 attempts
def admin_login():
    data = load_data(ADMIN_FILE)
    correct_user = data.get("username", "admin")
    correct_pass = data.get("password", "admin_password")

    print("\n--- ADMIN LOGIN ---")

    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username == correct_user and password == correct_pass:
            print("Login successful!\n")
            return True

        attempts += 1
        left = 3 - attempts
        print(f"Wrong credentials! {left} attempt(s) remaining.")

    print("Too many wrong attempts. Exiting program.")
    sys.exit(0)
