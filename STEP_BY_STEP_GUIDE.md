# Step-by-Step Beginner Guide: Building a Banking Management System (0 to 1)

This guide walks you through building the entire CLI Banking Management System from scratch. It explains what to do in every step, which folders and files to create, and the logic required in each part—without writing the code for you, so you can build and understand it yourself.

---

## Roadmap Overview

Here is the path from zero to a complete application:
1. **Folder & File Setup**: Preparing the workspace structure.
2. **Data Storage & File Handling**: Reading and saving JSON data safely.
3. **Validation Logic**: Checking user inputs before saving anything.
4. **Admin Authentication**: Creating a secure login screen with retry limits.
5. **Core Banking Operations**: Account creation, deposits, withdrawals, and balance enquiry.
6. **Customer Management**: Searching, listing, updating, and toggling account statuses.
7. **Reports & History**: Tracking transactions and generating bank statistics.
8. **Main Menu & Execution Loop**: Connecting all modules into an interactive application.

---

## Step 1: Project Setup (Folder & File Creation)

Start by creating your main project folder and organizing it so code and data stay separate.

1. Create a root project folder named `Banking - System`.
2. Inside the root folder, create two subfolders:
   - `data/` — Will hold your JSON database files.
   - `modules/` — Will hold all your Python logic split into manageable files.
3. Inside the `modules/` folder, create an empty file named `__init__.py`. This tells Python that the folder is a package so you can import functions across files.
4. Inside `modules/`, create these empty Python files:
   - `storage.py`
   - `validation.py`
   - `auth.py`
   - `banking.py`
   - `customer.py`
   - `reports.py`
5. Inside the root folder, create:
   - `main.py` — The entry point of your program.
   - `README.md` — Project documentation.

---

## Step 2: Storage & File Handling (`modules/storage.py`)

This file is responsible for saving and loading data to and from the disk.

### Tasks to Implement:
1. **Define File Paths**:
   - Determine the base directory dynamically using Python's `os.path` functions so the program works regardless of where you run it from.
   - Define paths to three JSON files inside the `data/` folder: `admin_data.json`, `customers.json`, and `transactions.json`.

2. **File Initialization Function**:
   - Check if the `data/` directory exists; if not, create it.
   - Check if `admin_data.json` exists; if missing, create it with a default username and password.
   - Check if `customers.json` exists; if missing, create it with an empty list (`[]`).
   - Check if `transactions.json` exists; if missing, create it with an empty list (`[]`).

3. **Data Loading Function**:
   - Open the target file in read mode.
   - Use Python's built-in `json.loads()` to convert the text back into Python lists or dictionaries.
   - Use a `try...except` block to catch `json.JSONDecodeError` so if someone accidentally corrupts a file, the program alerts the user and halts instead of crashing.

4. **Data Saving Function**:
   - Open the target file in write mode.
   - Use `json.dump()` with an indentation of 4 spaces so the JSON files remain easy to read by humans.

5. **Timestamp Helper**:
   - Use the `datetime` module to create a function that returns the current time formatted as `YYYY-MM-DD HH:MM:SS`.

---

## Step 3: Input Validation (`modules/validation.py`)

Never trust raw user input. This module contains simple functions that check inputs before the banking logic touches them. Each function should return a boolean (`True`/`False`) and an error message string.

### Validations to Build:
1. **Name Validation**:
   - Strip whitespace.
   - Ensure it is not empty.
   - Ensure length is at most 32 characters.

2. **Date of Birth Validation**:
   - Parse the string using `datetime.strptime` with format `DD/MM/YYYY`.
   - If parsing fails, return an error for invalid format/calendar date.
   - Compare the parsed date against today's date; reject dates in the future.

3. **Phone Number Validation**:
   - Ensure the string is exactly 10 characters and contains only digits (`.isdigit()`).
   - Loop through the existing customers list to ensure the phone number is not already registered to someone else.

4. **Aadhaar Number Validation**:
   - Ensure the string is exactly 12 characters and all numeric digits.
   - Check uniqueness across existing customers.

5. **PAN Card Validation**:
   - Convert input to uppercase.
   - Ensure it is exactly 10 characters.
   - Check the Indian PAN format: first 5 characters must be alphabetic, next 4 must be digits, and the last 1 must be alphabetic.
   - Check uniqueness across existing customers.

6. **Address Validation**:
   - Ensure the stripped text is not empty.

7. **Email Validation**:
   - Check for the presence of `@`.
   - Split by `@` into username and domain parts.
   - Verify that the username is not empty and that the domain contains a dot (`.`).
   - Check uniqueness across existing customers.

8. **Transaction Amount Validation**:
   - Ensure the input is not empty.
   - If a decimal point exists, split by `.` and ensure there are no more than 2 decimal digits.
   - Convert to `float` inside a `try...except` block.
   - Check that the number is strictly greater than zero.
   - Return the rounded number (2 decimal places).

---

## Step 4: Admin Authentication (`modules/auth.py`)

This module handles the login screen and enforces security limits.

### Tasks to Implement:
1. Load the admin credentials from `admin_data.json` using the storage module.
2. Initialize an attempt counter starting at 0 with a maximum of 3 attempts.
3. Use a `while` loop to prompt for username and password.
4. If both match the stored values, display a success message and return `True`.
5. If they do not match, increment the attempt counter, display the remaining attempts, and repeat the loop.
6. If 3 failed attempts are reached, display a security alert and terminate the program using `sys.exit(0)`.

---

## Step 5: Core Banking Operations (`modules/banking.py`)

This module handles accounts, deposits, withdrawals, and balance enquiries.

### Tasks to Implement:
1. **Helper Functions**:
   - `find_customer`: Loops through the customer list and returns the dictionary matching the entered account number, or `None` if not found.
   - `generate_acc_no`: Uses Python's `random.randint` to produce a random 10-digit number. Loops until the generated number does not exist in the current customers list.
   - `generate_txn_id`: Generates a unique transaction identifier string (e.g., `TXN` + random 6 digits).

2. **Create Account**:
   - Prompt for each customer field one by one inside `while True` loops.
   - Run each field through its respective validation function from `validation.py`. If invalid, print the error and re-prompt the same field.
   - Once all 8 fields are valid, generate a unique 10-digit account number.
   - Build a customer dictionary with initial balance `0.0`, status set to `"Active"`, and creation timestamp.
   - Append to the customer list and save to `customers.json`.
   - Print a success receipt showing the generated account number.

3. **Deposit Money**:
   - Ask for account number and locate the customer.
   - Verify the account exists and its status is `"Active"`.
   - Ask for deposit amount and validate it (positive, max 2 decimals).
   - Add amount to customer's current balance and round to 2 decimals.
   - Build a transaction record (Transaction ID, Account Number, Type: "Deposit", Amount, Previous Balance, New Balance, Timestamp, Status: "Success").
   - Save updated customer data to `customers.json` and append transaction record to `transactions.json`.
   - Display success message with new balance.

4. **Withdraw Money**:
   - Ask for account number and verify the account exists and is `"Active"`.
   - Ask for withdrawal amount and validate it.
   - Check that the customer has sufficient balance (`amount <= balance`). If not, display an error and exit the function without modifying data.
   - Deduct amount from balance.
   - Create a transaction record with Type: "Withdrawal".
   - Save updated customer and transaction records to their respective JSON files.
   - Display remaining balance.

5. **Balance Enquiry**:
   - Ask for account number, find customer, and display account number, name, status, and balance. (Read-only operation; modifies no data).

---

## Step 6: Customer Management (`modules/customer.py`)

This module provides tools to inspect and modify customer accounts.

### Tasks to Implement:
1. **View All Customers**:
   - Check if list is empty.
   - Print a formatted table showing Account Number, Name, Mobile, Email, and Status.
   - Keep sensitive details (Aadhaar and PAN) hidden in this overview list.

2. **Search by Account Number**:
   - Prompt for exact account number and print the matching customer's basic details.

3. **Search by Name**:
   - Prompt for a search string.
   - Loop over customers, convert both the search string and customer name to lowercase, and check if the search string is a substring (`if query in name.lower():`).
   - Display all matches in a table.

4. **Update Customer Details**:
   - Find customer by account number.
   - For each editable field (Name, Phone, Email, Address, Mother's Name), display current value and prompt for a new value.
   - If user presses Enter without typing anything, keep the existing value.
   - If user enters a new value, validate it before updating. When validating phone or email, make sure not to flag the customer's own existing value as a duplicate!
   - Save updated customer list to file.

5. **Activate / Deactivate Account**:
   - Find customer by account number.
   - If status is `"Active"`, ask confirmation to change to `"Inactive"`.
   - If status is `"Inactive"`, ask confirmation to change to `"Active"`.
   - Save changes to file.

6. **View Full Account Details**:
   - Dedicated administrative screen that displays all 12 stored fields for a single account, including full Aadhaar, PAN, and full address.

7. **Submenu Loop**:
   - Wrap these options in a numbered submenu with an option to return to the main dashboard.

---

## Step 7: Reports & Transaction History (`modules/reports.py`)

This module aggregates stored data for analysis.

### Tasks to Implement:
1. **Transaction Table Formatter**:
   - Helper function that prints a clean, aligned table of transaction items (ID, Account Number, Type, Amount, New Balance, Date/Time, Status).

2. **Transaction History Submenu**:
   - Option 1: Filter transactions matching a specific account number, reverse the list to show newest first, and print.
   - Option 2: Show all transactions across the entire bank, newest first.
   - Option 3: Return to main menu.

3. **Reports Submenu**:
   - Customer List Report (calls view all customers).
   - Transaction Report (prints all transactions).
   - Total Customers count (`len(customers)`).
   - Total Active Accounts count (count where `status == "Active"`).
   - Total Inactive Accounts count (count where `status == "Inactive"`).
   - Total Deposited Volume (sum `amount` where type is "Deposit" and status is "Success").
   - Total Withdrawn Volume (sum `amount` where type is "Withdrawal" and status is "Success").
   - Return to dashboard.

---

## Step 8: Main Application Loop (`main.py`)

This ties everything together into a clean, running application.

### Tasks to Implement:
1. Import the necessary functions from each module in the `modules/` package.
2. Define `show_dashboard()`:
   - Load customers and transactions from storage.
   - Display the main menu options (1: Create Account, 2: Deposit, 3: Withdraw, 4: Balance Enquiry, 5: Transaction History, 6: Customer Management, 7: Full Account Details, 8: Reports, 9: Logout, 0: Exit).
   - Take user input and use an `if / elif / else` ladder to call the corresponding function.
   - Handle invalid numbers gracefully with an error message.
   - Option 9 returns a `"logout"` string to exit the dashboard.
   - Option 0 calls `sys.exit(0)` to close the program.
3. Define `main()`:
   - Call `initialize_files()` once at startup.
   - Run a `while True` loop:
     - First, call `admin_login()`.
     - Once login succeeds, call `show_dashboard()`.
     - If the dashboard returns `"logout"`, loop repeats and prompts for login again.
4. Add the standard execution check: `if __name__ == "__main__": main()`.

---

## Step 9: Testing Your Application

Once built, verify your program step-by-step:

1. **First Run**: Delete the `data/` folder and run `python main.py`. Check that the `data/` folder and all 3 JSON files are created automatically.
2. **Login Test**: Enter wrong credentials 3 times to make sure the app terminates. Run again with correct credentials (`admin` / `admin_password`) to reach the dashboard.
3. **Account Creation**: Create 2 customer accounts. Verify:
   - Invalid dates (future or non-existent calendar dates) are rejected.
   - Duplicate phone, Aadhaar, PAN, and email are rejected.
   - Account numbers generated are unique 10 digits.
4. **Deposit & Withdrawal**:
   - Deposit ₹5,000 into Account 1. Check updated balance.
   - Try to withdraw ₹6,000 (should fail due to insufficient funds).
   - Withdraw ₹2,000 (should succeed, remaining balance ₹3,000).
5. **Persistence**:
   - Exit the application (`0`).
   - Inspect `data/customers.json` and `data/transactions.json` to confirm your records are intact.
   - Restart the app and run a Balance Enquiry to ensure data was loaded from disk.
6. **Account Deactivation**:
   - Deactivate Account 1.
   - Try to deposit or withdraw (both must be rejected).
   - Re-activate Account 1 and verify transactions work again.
7. **Reports**:
   - Open Reports and verify that customer counts and deposit/withdrawal totals match your actions.
