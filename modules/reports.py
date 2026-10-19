from modules.customer import view_all_customers


# prints a formatted table of transaction records
def print_transactions(txns):
    if not txns:
        print("No transactions found.")
        return

    print("\n" + "-" * 90)
    print(f"{'TXN ID':<10} | {'Acc No':<12} | {'Type':<11} | {'Amount':<10} | {'New Bal':<10} | {'Date & Time':<19} | {'Status'}")
    print("-" * 90)

    for t in txns:
        print(f"{t['transaction_id']:<10} | {t['account_number']:<12} | {t['transaction_type']:<11} | Rs.{t['amount']:<7.2f} | Rs.{t['new_balance']:<7.2f} | {t['date_time']:<19} | {t['status']}")
    print("-" * 90)


# submenu to view transactions by account or all newest first
def transaction_history(transactions):
    while True:
        print("\n--- TRANSACTION HISTORY ---")
        print("1. View Transactions for Specific Account")
        print("2. View All Transactions")
        print("3. Back to Dashboard")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            acc_no = input("Enter Account Number: ").strip()
            acc_txns = []
            for t in transactions:
                if t["account_number"] == acc_no:
                    acc_txns.append(t)

            acc_txns_reversed = list(reversed(acc_txns))
            print_transactions(acc_txns_reversed)

        elif choice == "2":
            all_reversed = list(reversed(transactions))
            print_transactions(all_reversed)

        elif choice == "3":
            break
        else:
            print("Invalid choice, choose 1, 2, or 3.")


# submenu for viewing customer stats and financial totals
def show_reports(customers, transactions):
    while True:
        print("\n--- REPORTS MENU ---")
        print("1. Customer List Report")
        print("2. Transaction Report")
        print("3. Total Customers")
        print("4. Total Active Accounts")
        print("5. Total Inactive Accounts")
        print("6. Total Deposited Amount")
        print("7. Total Withdrawn Amount")
        print("8. Back to Dashboard")

        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            view_all_customers(customers)

        elif choice == "2":
            print_transactions(transactions)

        elif choice == "3":
            print(f"\nTotal Customers: {len(customers)}")

        elif choice == "4":
            count = 0
            for c in customers:
                if c["status"] == "Active":
                    count += 1
            print(f"\nTotal Active Accounts: {count}")

        elif choice == "5":
            count = 0
            for c in customers:
                if c["status"] == "Inactive":
                    count += 1
            print(f"\nTotal Inactive Accounts: {count}")

        elif choice == "6":
            total = 0.0
            for t in transactions:
                if t["transaction_type"] == "Deposit" and t["status"] == "Success":
                    total += t["amount"]
            print(f"\nTotal Money Deposited: Rs. {total:.2f}")

        elif choice == "7":
            total = 0.0
            for t in transactions:
                if t["transaction_type"] == "Withdrawal" and t["status"] == "Success":
                    total += t["amount"]
            print(f"\nTotal Money Withdrawn: Rs. {total:.2f}")

        elif choice == "8":
            break
        else:
            print("Invalid choice, choose 1 to 8.")
