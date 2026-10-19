import random
from modules.storage import (
    CUSTOMERS_FILE,
    TRANSACTIONS_FILE,
    save_data,
    get_current_time
)
from modules.validation import (
    validate_name,
    validate_dob,
    validate_phone,
    validate_aadhaar,
    validate_pan,
    validate_address,
    validate_email,
    validate_amount
)


# looks up a customer by their account number
def find_customer(customers, acc_no):
    acc_no = acc_no.strip()
    for c in customers:
        if c["account_number"] == acc_no:
            return c
    return None


# generates a unique 10-digit random account number
def generate_acc_no(customers):
    existing = []
    for c in customers:
        existing.append(c["account_number"])

    while True:
        num = str(random.randint(1000000000, 9999999999))
        if num not in existing:
            return num


# generates a unique transaction id like TXN123456
def generate_txn_id(transactions):
    existing = []
    for t in transactions:
        existing.append(t["transaction_id"])

    while True:
        txn_id = "TXN" + str(random.randint(100000, 999999))
        if txn_id not in existing:
            return txn_id


# takes all inputs, validates them, and creates a new account with 0 balance
def create_account(customers):
    print("\n--- CREATE CUSTOMER ACCOUNT ---")

    # Name
    while True:
        name = input("Enter Name: ").strip()
        ok, msg = validate_name(name)
        if ok:
            break
        print(msg)

    # Date of Birth
    while True:
        dob = input("Enter Date of Birth (DD/MM/YYYY): ").strip()
        ok, msg = validate_dob(dob)
        if ok:
            break
        print(msg)

    # Phone
    while True:
        phone = input("Enter 10-digit Phone: ").strip()
        ok, msg = validate_phone(phone, customers)
        if ok:
            break
        print(msg)

    # Aadhaar
    while True:
        aadhaar = input("Enter 12-digit Aadhaar: ").strip()
        ok, msg = validate_aadhaar(aadhaar, customers)
        if ok:
            break
        print(msg)

    # PAN
    while True:
        pan = input("Enter PAN (e.g. ABCDE1234F): ").strip().upper()
        ok, msg = validate_pan(pan, customers)
        if ok:
            break
        print(msg)

    # Address
    while True:
        address = input("Enter Address: ").strip()
        ok, msg = validate_address(address)
        if ok:
            break
        print(msg)

    # Email
    while True:
        email = input("Enter Email: ").strip()
        ok, msg = validate_email(email, customers)
        if ok:
            break
        print(msg)

    # Mother's Name
    while True:
        mother = input("Enter Mother's Name: ").strip()
        ok, msg = validate_name(mother)
        if ok:
            break
        print(msg)

    acc_no = generate_acc_no(customers)
    created_at = get_current_time()

    new_customer = {
        "account_number": acc_no,
        "name": name,
        "date_of_birth": dob,
        "mobile": phone,
        "aadhaar": aadhaar,
        "pan": pan,
        "address": address,
        "email": email,
        "mother_name": mother,
        "balance": 0.0,
        "created_at": created_at,
        "status": "Active"
    }

    customers.append(new_customer)
    save_data(CUSTOMERS_FILE, customers)

    print("\nAccount created successfully!")
    print(f"Account Number: {acc_no}")
    print(f"Name: {name}")
    print("Initial Balance: Rs. 0.00")


# deposits money into an active account and records the transaction
def deposit_money(customers, transactions):
    print("\n--- DEPOSIT MONEY ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Account not found.")
        return

    if cust["status"] != "Active":
        print("Account is Inactive. Deposit not allowed.")
        return

    print(f"Customer: {cust['name']} | Current Balance: Rs. {cust['balance']:.2f}")
    amt_str = input("Enter Amount to Deposit: ").strip()
    ok, amt, msg = validate_amount(amt_str)
    if not ok:
        print(msg)
        return

    old_bal = cust["balance"]
    new_bal = round(old_bal + amt, 2)
    cust["balance"] = new_bal

    txn_id = generate_txn_id(transactions)
    time_now = get_current_time()

    txn = {
        "transaction_id": txn_id,
        "account_number": cust["account_number"],
        "transaction_type": "Deposit",
        "amount": amt,
        "previous_balance": old_bal,
        "new_balance": new_bal,
        "date_time": time_now,
        "status": "Success"
    }

    save_data(CUSTOMERS_FILE, customers)
    transactions.append(txn)
    save_data(TRANSACTIONS_FILE, transactions)

    print(f"Deposited Rs. {amt:.2f} successfully.")
    print(f"Transaction ID: {txn_id}")
    print(f"New Balance: Rs. {new_bal:.2f}")


# withdraws money if balance is sufficient and records the transaction
def withdraw_money(customers, transactions):
    print("\n--- WITHDRAW MONEY ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Account not found.")
        return

    if cust["status"] != "Active":
        print("Account is Inactive. Withdrawal not allowed.")
        return

    print(f"Customer: {cust['name']} | Current Balance: Rs. {cust['balance']:.2f}")
    amt_str = input("Enter Amount to Withdraw: ").strip()
    ok, amt, msg = validate_amount(amt_str)
    if not ok:
        print(msg)
        return

    if amt > cust["balance"]:
        print(f"Insufficient funds! You only have Rs. {cust['balance']:.2f}")
        return

    old_bal = cust["balance"]
    new_bal = round(old_bal - amt, 2)
    cust["balance"] = new_bal

    txn_id = generate_txn_id(transactions)
    time_now = get_current_time()

    txn = {
        "transaction_id": txn_id,
        "account_number": cust["account_number"],
        "transaction_type": "Withdrawal",
        "amount": amt,
        "previous_balance": old_bal,
        "new_balance": new_bal,
        "date_time": time_now,
        "status": "Success"
    }

    save_data(CUSTOMERS_FILE, customers)
    transactions.append(txn)
    save_data(TRANSACTIONS_FILE, transactions)

    print(f"Withdrawn Rs. {amt:.2f} successfully.")
    print(f"Transaction ID: {txn_id}")
    print(f"Remaining Balance: Rs. {new_bal:.2f}")


# shows current balance and status without modifying any data
def balance_enquiry(customers):
    print("\n--- BALANCE ENQUIRY ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Account not found.")
        return

    print(f"Account Number: {cust['account_number']}")
    print(f"Name          : {cust['name']}")
    print(f"Status        : {cust['status']}")
    print(f"Balance       : Rs. {cust['balance']:.2f}")
