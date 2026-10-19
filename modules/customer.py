from modules.storage import CUSTOMERS_FILE, save_data
from modules.banking import find_customer
from modules.validation import (
    validate_name,
    validate_phone,
    validate_address,
    validate_email
)


def view_all_customers(customers):
    if not customers:
        print("No customers found.")
        return

    print("\n" + "-" * 75)
    print(f"{'Acc No':<12} | {'Name':<18} | {'Mobile':<12} | {'Email':<20} | {'Status'}")
    print("-" * 75)

    for c in customers:
        acc = c["account_number"]
        name = c["name"]
        mobile = c["mobile"]
        email = c["email"]
        status = c["status"]
        print(f"{acc:<12} | {name:<18} | {mobile:<12} | {email:<20} | {status}")
    print("-" * 75)


def search_by_acc_no(customers):
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Customer not found.")
        return

    print(f"\nAccount Number: {cust['account_number']}")
    print(f"Name          : {cust['name']}")
    print(f"Mobile        : {cust['mobile']}")
    print(f"Email         : {cust['email']}")
    print(f"Balance       : Rs. {cust['balance']:.2f}")
    print(f"Status        : {cust['status']}")


def search_by_name(customers):
    query = input("Enter Name to search: ").strip().lower()
    if not query:
        print("Search text cannot be blank.")
        return

    found = []
    for c in customers:
        if query in c["name"].lower():
            found.append(c)

    if not found:
        print("No matching customer found.")
        return

    print(f"\nFound {len(found)} matching customer(s):")
    view_all_customers(found)


def update_customer_details(customers):
    print("\n--- UPDATE CUSTOMER DETAILS ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Customer not found.")
        return

    print(f"Editing: {cust['name']} (Press Enter to keep current value)")

    # Name
    new_name = input(f"New Name [{cust['name']}]: ").strip()
    if new_name:
        ok, msg = validate_name(new_name)
        if ok:
            cust["name"] = new_name
        else:
            print(msg)

    # Phone
    new_phone = input(f"New Phone [{cust['mobile']}]: ").strip()
    if new_phone:
        ok, msg = validate_phone(new_phone, customers, current_acc=cust["account_number"])
        if ok:
            cust["mobile"] = new_phone
        else:
            print(msg)

    # Email
    new_email = input(f"New Email [{cust['email']}]: ").strip()
    if new_email:
        ok, msg = validate_email(new_email, customers, current_acc=cust["account_number"])
        if ok:
            cust["email"] = new_email
        else:
            print(msg)

    # Address
    new_address = input(f"New Address [{cust['address']}]: ").strip()
    if new_address:
        ok, msg = validate_address(new_address)
        if ok:
            cust["address"] = new_address
        else:
            print(msg)

    # Mother's name
    new_mother = input(f"New Mother's Name [{cust['mother_name']}]: ").strip()
    if new_mother:
        ok, msg = validate_name(new_mother)
        if ok:
            cust["mother_name"] = new_mother
        else:
            print(msg)

    save_data(CUSTOMERS_FILE, customers)
    print("Customer details updated successfully.")


def toggle_account_status(customers):
    print("\n--- ACTIVATE / DEACTIVATE ACCOUNT ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Account not found.")
        return

    print(f"Customer: {cust['name']} | Current Status: {cust['status']}")

    if cust["status"] == "Active":
        ans = input("Deactivate this account? (y/n): ").strip().lower()
        if ans == "y" or ans == "yes":
            cust["status"] = "Inactive"
            save_data(CUSTOMERS_FILE, customers)
            print("Account is now Inactive.")
    else:
        ans = input("Activate this account? (y/n): ").strip().lower()
        if ans == "y" or ans == "yes":
            cust["status"] = "Active"
            save_data(CUSTOMERS_FILE, customers)
            print("Account is now Active.")


def view_account_details(customers):
    print("\n--- VIEW FULL ACCOUNT DETAILS ---")
    acc_no = input("Enter Account Number: ").strip()
    cust = find_customer(customers, acc_no)

    if not cust:
        print("Account not found.")
        return

    print(f"Account Number : {cust['account_number']}")
    print(f"Name           : {cust['name']}")
    print(f"Date of Birth  : {cust['date_of_birth']}")
    print(f"Mobile         : {cust['mobile']}")
    print(f"Aadhaar        : {cust['aadhaar']}")
    print(f"PAN            : {cust['pan']}")
    print(f"Address        : {cust['address']}")
    print(f"Email          : {cust['email']}")
    print(f"Mother's Name  : {cust['mother_name']}")
    print(f"Balance        : Rs. {cust['balance']:.2f}")
    print(f"Status         : {cust['status']}")
    print(f"Created At     : {cust['created_at']}")


def customer_management(customers):
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. View All Customers")
        print("2. Search Customer by Account Number")
        print("3. Search Customer by Name")
        print("4. Update Customer Details")
        print("5. Activate / Deactivate Account")
        print("6. Back to Dashboard")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            view_all_customers(customers)
        elif choice == "2":
            search_by_acc_no(customers)
        elif choice == "3":
            search_by_name(customers)
        elif choice == "4":
            update_customer_details(customers)
        elif choice == "5":
            toggle_account_status(customers)
        elif choice == "6":
            break
        else:
            print("Invalid choice, please enter 1 to 6.")
