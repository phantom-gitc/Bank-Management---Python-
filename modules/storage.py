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


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def initialize_files():
    # make data folder if missing
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    # create admin file with default login
    if not os.path.exists(ADMIN_FILE):
        default_admin = {
            "username": "admin",
            "password": "admin_password"
        }
        with open(ADMIN_FILE, "w") as f:
            json.dump(default_admin, f, indent=4)

    # create empty customers list
    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "w") as f:
            json.dump([], f, indent=4)

    # create empty transactions list
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w") as f:
            json.dump([], f, indent=4)


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


def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
