import sys
from modules.storage import (
    CUSTOMERS_FILE,
    TRANSACTIONS_FILE,
    initialize_files,
    load_data
)
from modules.auth import admin_login
from modules.banking import (
    create_account,
    deposit_money,
    withdraw_money,
    balance_enquiry
)
from modules.customer import customer_management, view_account_details
from modules.reports import transaction_history, show_reports


# displays the main dashboard menu and handles user selection
def show_dashboard():
    customers = load_data(CUSTOMERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    while True:
        print("\n==============================")
        print("  BANKING MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Create Customer Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Balance Enquiry")
        print("5. Transaction History")
        print("6. Customer Management")
        print("7. View Full Account Details")
        print("8. Reports")
        print("9. Logout")
        print("0. Exit")
        print("==============================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_account(customers)
        elif choice == "2":
            deposit_money(customers, transactions)
        elif choice == "3":
            withdraw_money(customers, transactions)
        elif choice == "4":
            balance_enquiry(customers)
        elif choice == "5":
            transaction_history(transactions)
        elif choice == "6":
            customer_management(customers)
        elif choice == "7":
            view_account_details(customers)
        elif choice == "8":
            show_reports(customers, transactions)
        elif choice == "9":
            print("Logged out successfully.")
            return "logout"
        elif choice == "0":
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice! Enter a number between 0 and 9.")


# runs setup, handles admin login, and keeps the program running
def main():
    initialize_files()

    while True:
        admin_login()
        result = show_dashboard()
        if result == "logout":
            continue


if __name__ == "__main__":
    main()
