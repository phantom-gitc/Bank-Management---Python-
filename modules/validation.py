import datetime


# checks that the name is not empty and within 32 characters
def validate_name(name):
    clean_name = name.strip()
    if len(clean_name) == 0:
        return False, "Name cannot be empty."
    if len(clean_name) > 32:
        return False, "Name cannot be longer than 32 characters."
    return True, ""


# checks that DOB is in DD/MM/YYYY format and not in the future
def validate_dob(dob_str):
    dob_str = dob_str.strip()
    try:
        birth_date = datetime.datetime.strptime(dob_str, "%d/%m/%Y").date()
    except ValueError:
        return False, "Invalid date format. Use DD/MM/YYYY (e.g. 15/08/2000)."

    today = datetime.date.today()
    if birth_date > today:
        return False, "Date of birth cannot be in the future."

    return True, ""


# checks that phone number has 10 digits and is not already registered
def validate_phone(phone, customers, current_acc=None):
    phone = phone.strip()
    if len(phone) != 10 or not phone.isdigit():
        return False, "Phone number must be exactly 10 digits."

    for c in customers:
        if current_acc and c["account_number"] == current_acc:
            continue
        if c["mobile"] == phone:
            return False, "This phone number is already registered."

    return True, ""


# checks that Aadhaar is 12 digits and unique
def validate_aadhaar(aadhaar, customers):
    aadhaar = aadhaar.strip()
    if len(aadhaar) != 12 or not aadhaar.isdigit():
        return False, "Aadhaar number must be exactly 12 digits."

    for c in customers:
        if c["aadhaar"] == aadhaar:
            return False, "This Aadhaar is already registered."

    return True, ""


# checks standard Indian PAN format (5 letters, 4 numbers, 1 letter) and uniqueness
def validate_pan(pan, customers):
    pan = pan.strip().upper()
    if len(pan) != 10:
        return False, "PAN must be 10 characters long (e.g. ABCDE1234F)."

    first_part = pan[:5]
    middle_part = pan[5:9]
    last_char = pan[9]

    if not first_part.isalpha() or not middle_part.isdigit() or not last_char.isalpha():
        return False, "Invalid PAN format. Example: ABCDE1234F"

    for c in customers:
        if c["pan"] == pan:
            return False, "This PAN is already registered."

    return True, ""


# checks that address is not blank
def validate_address(address):
    if len(address.strip()) == 0:
        return False, "Address cannot be empty."
    return True, ""


# checks basic email format with username, @, domain and uniqueness
def validate_email(email, customers, current_acc=None):
    email = email.strip()
    if "@" not in email:
        return False, "Email must contain '@'."

    parts = email.split("@")
    if len(parts) != 2:
        return False, "Invalid email format."

    username, domain = parts[0], parts[1]
    if len(username) == 0:
        return False, "Email username cannot be empty."

    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False, "Email must have a valid domain (e.g. gmail.com)."

    for c in customers:
        if current_acc and c["account_number"] == current_acc:
            continue
        if c["email"].lower() == email.lower():
            return False, "This email is already registered."

    return True, ""


# checks that deposit or withdrawal amount is a positive number with max 2 decimals
def validate_amount(amount_str):
    amount_str = amount_str.strip()
    if not amount_str:
        return False, 0.0, "Amount cannot be blank."

    if "." in amount_str:
        parts = amount_str.split(".")
        if len(parts) != 2:
            return False, 0.0, "Invalid amount."
        if len(parts[1]) > 2:
            return False, 0.0, "Amount cannot have more than 2 decimal places."

    try:
        num = float(amount_str)
    except ValueError:
        return False, 0.0, "Please enter a valid number."

    if num <= 0:
        return False, 0.0, "Amount must be greater than 0."

    return True, round(num, 2), ""
