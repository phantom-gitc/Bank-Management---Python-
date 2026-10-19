# Banking Management System - Application Flow Diagram

This document explains **behind the scenes** how the entire Banking Management System works, from startup to data persistence. 

All diagrams use standard Mermaid syntax and will render visually inside VS Code or GitHub Markdown preview (`Ctrl + Shift + V` in VS Code).

---

## 1. High-Level System Architecture & Data Flow

Here is how the files talk to each other and how data moves into the JSON storage:

```mermaid
graph TD
    User([Bank Administrator]) <--> Main[main.py: App Controller & Menu]
    
    subgraph "Application Modules"
        Main --> Auth[modules/auth.py: Authentication]
        Main --> Banking[modules/banking.py: Core Operations]
        Main --> Customer[modules/customer.py: Management]
        Main --> Reports[modules/reports.py: Reports & History]
        
        Banking --> Valid[modules/validation.py: Input Rules]
        Customer --> Valid
        
        Banking --> Storage[modules/storage.py: File I/O]
        Customer --> Storage
        Auth --> Storage
    end

    subgraph "Persistent Storage (Disk)"
        Storage <--> AdminJSON[(data/admin_data.json)]
        Storage <--> CustJSON[(data/customers.json)]
        Storage <--> TxnJSON[(data/transactions.json)]
    end
```

---

## 2. Complete Program Lifecycle Flow

What happens when you type `python main.py` in your terminal:

```mermaid
flowchart TD
    Start([Run python main.py]) --> Init[initialize_files: Check /data folder & JSON files]
    Init --> CheckFiles{Do JSON files exist?}
    CheckFiles -- No --> CreateDefaults[Create data folder & default JSON files] --> LoginScreen
    CheckFiles -- Yes --> LoginScreen[Prompt Admin Login]

    LoginScreen --> CheckCreds{Username & Password match?}
    CheckCreds -- No --> FailAttempt[Failed Attempts + 1]
    FailAttempt --> Max3{Attempts >= 3?}
    Max3 -- Yes --> LockExit([Alert & Exit Program])
    Max3 -- No --> LoginScreen

    CheckCreds -- Yes --> LoadData[Load customers.json & transactions.json into Memory]
    LoadData --> Dashboard[Display Admin Dashboard Menu 0-9]

    Dashboard --> Choice{User Choice}
    Choice -- 1 --> F1[Create Account] --> SaveAndReturn[Save to JSON & Return]
    Choice -- 2 --> F2[Deposit Money] --> SaveAndReturn
    Choice -- 3 --> F3[Withdraw Money] --> SaveAndReturn
    Choice -- 4 --> F4[Balance Enquiry] --> Dashboard
    Choice -- 5 --> F5[Transaction History] --> Dashboard
    Choice -- 6 --> F6[Customer Management] --> SaveAndReturn
    Choice -- 7 --> F7[View Full Details] --> Dashboard
    Choice -- 8 --> F8[Reports Menu] --> Dashboard
    Choice -- 9 --> Logout[Logout: Return to Login Screen] --> LoginScreen
    Choice -- 0 --> ExitApp([Exit Application])

    SaveAndReturn --> Dashboard
```

---

## 3. Account Creation Behind the Scenes (`create_account`)

How each field is prompted, validated, and saved with a unique 10-digit number:

```mermaid
flowchart TD
    StartAcc([Start Account Creation]) --> InName[/Input Name/]
    InName --> VName{Valid Name?}
    VName -- No --> InName

    VName -- Yes --> InDOB[/Input Date of Birth/]
    InDOB --> VDOB{Valid Calendar Date & Not Future?}
    VDOB -- No --> InDOB

    VDOB -- Yes --> InPhone[/Input 10-digit Phone/]
    InPhone --> VPhone{10 Digits & Not Duplicate?}
    VPhone -- No --> InPhone

    VPhone -- Yes --> InAadhaar[/Input 12-digit Aadhaar/]
    InAadhaar --> VAadhaar{12 Digits & Unique?}
    VAadhaar -- No --> InAadhaar

    VAadhaar -- Yes --> InPAN[/Input 10-char PAN/]
    InPAN --> VPAN{5 letters + 4 digits + 1 letter & Unique?}
    VPAN -- No --> InPAN

    VPAN -- Yes --> InAddr[/Input Address/]
    InAddr --> VAddr{Not Empty?}
    VAddr -- No --> InAddr

    VAddr -- Yes --> InEmail[/Input Email/]
    InEmail --> VEmail{Valid @ and domain & Unique?}
    VEmail -- No --> InEmail

    VEmail -- Yes --> InMother[/Input Mother's Name/]
    InMother --> VMother{Not Empty?}
    VMother -- No --> InMother

    VMother -- Yes --> GenAcc[Generate Random 10-Digit Account Number]
    GenAcc --> CheckAccDup{Account number already used?}
    CheckAccDup -- Yes --> GenAcc
    CheckAccDup -- No --> BuildCustDict[Construct Customer Dictionary:\nbalance = 0.0, status = 'Active', timestamp]

    BuildCustDict --> SaveCust[Append to customers list & write to data/customers.json]
    SaveCust --> PrintReceipt[/Print Account Creation Receipt/] --> EndAcc([Return to Dashboard])
```

---

## 4. Deposit & Withdrawal Flow

How money operations validate accounts, check funds, update balance, and record audit trails:

```mermaid
flowchart TD
    StartMoney([Deposit / Withdraw Selected]) --> InputAcc[/Enter Account Number/]
    InputAcc --> FindCust{Account exists?}
    FindCust -- No --> ErrAcc[Print 'Account not found'] --> EndMoney([Return])

    FindCust -- Yes --> CheckStatus{Status is 'Active'?}
    CheckStatus -- No --> ErrInactive[Print 'Account is Inactive'] --> EndMoney

    CheckStatus -- Yes --> InputAmt[/Enter Amount/]
    InputAmt --> ValAmt{Amount > 0 and <= 2 Decimals?}
    ValAmt -- No --> ErrAmt[Print Invalid Amount Error] --> EndMoney

    ValAmt -- Yes --> IsDeposit{Operation Type?}
    
    IsDeposit -- Deposit --> AddBal[New Balance = Old Balance + Amount]
    
    IsDeposit -- Withdraw --> CheckFunds{Amount <= Balance?}
    CheckFunds -- No --> ErrFunds[Print 'Insufficient Funds'] --> EndMoney
    CheckFunds -- Yes --> SubBal[New Balance = Old Balance - Amount]

    AddBal --> CreateTxn[Generate Unique TXN ID & Timestamp]
    SubBal --> CreateTxn

    CreateTxn --> BuildTxnDict[Construct Transaction Record Dictionary]
    BuildTxnDict --> SaveCustJSON[Update customers.json on disk]
    SaveCustJSON --> SaveTxnJSON[Append record to transactions.json on disk]
    SaveTxnJSON --> DisplaySuccess[/Display Updated Balance & Transaction ID/] --> EndMoney
```

---

## 5. Customer Management Submenu Flow

```mermaid
flowchart TD
    Menu([Customer Management Menu]) --> SubChoice{Select Option}

    SubChoice -- 1 --> ViewAll[Loop customers: Print Account, Name, Phone, Email, Status\nMask Aadhaar & PAN] --> Menu
    
    SubChoice -- 2 --> SearchAcc[Input Account Number -> Find exact match -> Print details] --> Menu
    
    SubChoice -- 3 --> SearchName[Input search string -> Case-insensitive partial search -> Display list] --> Menu
    
    SubChoice -- 4 --> UpdateCust[Input Account Number -> Find customer]
    UpdateCust --> FieldPrompt[For each editable field:\nPress Enter = Keep current value\nType new value = Validate & update]
    FieldPrompt --> SaveUpdatedCust[Save updated list to customers.json] --> Menu

    SubChoice -- 5 --> ToggleStatus[Input Account Number -> Toggle Active <-> Inactive -> Save to JSON] --> Menu
    
    SubChoice -- 6 --> BackDash([Return to Main Dashboard])
```

---

## 6. Reports & Aggregation Flow

```mermaid
flowchart TD
    ReportsStart([Reports Menu]) --> RepChoice{Select Report}

    RepChoice -- 1 --> RepCustList[Display All Customers Table] --> ReportsStart
    RepChoice -- 2 --> RepTxnList[Display All Transactions Table] --> ReportsStart
    RepChoice -- 3 --> CountCust[Calculate len(customers) -> Display total] --> ReportsStart
    RepChoice -- 4 --> CountActive[Count customers where status == 'Active'] --> ReportsStart
    RepChoice -- 5 --> CountInactive[Count customers where status == 'Inactive'] --> ReportsStart
    RepChoice -- 6 --> SumDeposits[Sum transaction amounts where type == 'Deposit'] --> ReportsStart
    RepChoice -- 7 --> SumWithdraws[Sum transaction amounts where type == 'Withdrawal'] --> ReportsStart
    RepChoice -- 8 --> BackMain([Return to Main Dashboard])
```
