import json
import os
import sys
import datetime

# paths for data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

ADMIN_FILE = os.path.join(DATA_DIR, "admin_data.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")


# returns the current date and time as a string
def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# creates the data folder and starter json files if they don't exist yet
def initialize_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ADMIN_FILE):
        default_admin = {
            "username": "admin",
            "password": "admin_password"
        }
        with open(ADMIN_FILE, "w") as f:
            json.dump(default_admin, f, indent=4)

    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "w") as f:
            json.dump([], f, indent=4)

    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w") as f:
            json.dump([], f, indent=4)


# reads a json file and returns its content as a python list or dict
def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                if "admin" in file_path:
                    return {}
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is corrupted.")
        sys.exit(1)


# writes python data to a json file with clean 4-space indentation
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
