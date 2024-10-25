import pandas as pd
import random
from datetime import datetime, timedelta

# Define common realistic companies for various categories
companies = {
    "Salary Credited": ["TCS Ltd", "Infosys Ltd", "Wipro Ltd", "Reliance Industries Ltd", "HDFC Bank Ltd"],
    "Rent Payment": ["Property Owner - Rahul Verma", "Property Owner - Seema Agarwal", "Apartment Lease - Skyline Rentals"],
    "Health Insurance Premium": ["Star Health Insurance", "ICICI Lombard", "HDFC ERGO", "Max Bupa Insurance"],
    "Medical Expenses": ["Apollo Hospitals", "Fortis Healthcare", "Dr. Lal Pathlabs", "Medanta Hospital", "Max Healthcare"],
    "Home Loan EMI Payment": ["HDFC Ltd", "ICICI Bank Ltd", "SBI Home Loans", "Axis Bank Ltd"],
    "Educational Loan Interest": ["Bank of Baroda", "State Bank of India", "Punjab National Bank", "IDFC First Bank"],
    "Charitable Donation": ["CRY India", "Helpage India", "Save the Children", "Smile Foundation"],
    "Electricity Bill Payment": ["Tata Power Ltd", "BSES Rajdhani", "Adani Power", "Torrent Power"],
    "Internet Bill Payment": ["Airtel Broadband", "ACT Fibernet", "Jio Fiber", "BSNL Broadband"],
    "Mutual Fund Investment": ["HDFC Mutual Fund", "SBI Mutual Fund", "Axis Mutual Fund", "ICICI Prudential Mutual Fund"],
    "Stock Market Transaction": ["Zerodha Brokerage", "ICICI Direct", "HDFC Securities", "Motilal Oswal Financial Services"],
    "PF Contribution": ["EPFO Contribution", "Employer Provident Fund - Reliance Ltd"],
    "Provident Fund Withdrawal": ["EPFO Withdrawal"],
    "LIC Premium Payment": ["LIC of India", "SBI Life Insurance", "Max Life Insurance", "HDFC Life Insurance"],
    "HRA Adjustment": ["Internal Payroll Adjustment - TCS Ltd", "Internal Payroll Adjustment - Infosys Ltd"],
    "Cash Withdrawal ATM": ["HDFC Bank ATM", "SBI ATM", "ICICI Bank ATM", "Axis Bank ATM"],
    "Income Tax Refund": ["Income Tax Department - Govt of India"],
    "School Tuition Fees": ["DPS School Fees", "Ryan International School Fees", "The Heritage School Fees", "National Public School Fees"],
    "Preventive Health Checkup": ["Dr. Lal Pathlabs", "Max Healthcare", "SRL Diagnostics", "Apollo Diagnostics"],
    "Senior Citizen Medical Expense": ["Fortis Healthcare", "Medanta Hospital", "Apollo Hospitals", "Max Healthcare"],
    "Interest Income on Savings": ["SBI Savings Interest", "HDFC Bank Savings Interest", "ICICI Bank Savings Interest", "Axis Bank Savings Interest"],
    "Grocery Store Purchase": ["Big Bazaar", "DMart", "Spencer's Retail", "Reliance Fresh"],
    "Car Loan EMI Payment": ["HDFC Bank Car Loan", "SBI Car Loan", "ICICI Bank Car Loan", "Axis Bank Car Loan"],
    "Fixed Deposit Created": ["HDFC Bank FD", "SBI FD", "ICICI Bank FD", "Axis Bank FD"],
    "Fixed Deposit Matured": ["HDFC Bank FD Maturity", "SBI FD Maturity", "ICICI Bank FD Maturity", "Axis Bank FD Maturity"],
    "Travel Reimbursement": ["Company Reimbursement - TCS Ltd", "Company Reimbursement - Infosys Ltd"],
    "Gift Received": ["Gift Transfer - Mr. Ajay Sharma", "Gift Transfer - Ms. Ritu Verma"],
    "Professional Fees Received": ["Consulting Payment - Infosys Ltd", "Consulting Payment - Wipro Ltd", "Consulting Payment - TCS Ltd"],
    "Investment in NPS": ["National Pension Scheme Investment - SBI", "National Pension Scheme Investment - ICICI"],
    "LTA Claimed": ["LTA Claim - TCS Ltd", "LTA Claim - Infosys Ltd"]
}

# Generate a random date within a specific range
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Generate synthetic bank statement
def generate_statement(num_transactions=100000):
    statement = []
    balance = 50000  # Starting balance
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    for i in range(1, num_transactions + 1):
        # Generate a realistic date
        transaction_date = random_date(start_date, end_date)
        
        # Choose a random category and narration
        narration_category = random.choice(list(companies.keys()))
        narration = random.choice(companies[narration_category])
        
        # Determine debit and credit amounts based on the category
        debit = 0
        credit = 0
        if "Credited" in narration_category or "Received" in narration_category or "Matured" in narration_category or "Refund" in narration_category:
            credit = round(random.uniform(5000, 80000), 2) if narration_category == "Salary Credited" else round(random.uniform(500, 20000), 2)
        elif "EMI" in narration_category or "Payment" in narration_category or "Bill" in narration_category or "Expenses" in narration_category or "Investment" in narration_category or "Fee" in narration_category:
            # Ensure debit doesn't exceed available balance
            max_debit = min(round(random.uniform(1000, 30000), 2), balance)
            debit = max_debit
        else:
            # Small, everyday expenses
            max_debit = min(round(random.uniform(100, 5000), 2), balance)
            debit = max_debit

        # Prevent balance from going negative
        if debit > balance:
            continue  # Skip this transaction if balance is insufficient

        # Adjust balance
        if debit > 0:
            balance -= debit
        else:
            balance += credit

        # Simulate a salary credit once a month to keep the balance positive
        if i % 30 == 0 and balance < 20000:
            salary_credit = round(random.uniform(50000, 80000), 2)
            narration = "Salary Credited - " + random.choice(companies["Salary Credited"])
            statement.append({
                "Date": transaction_date.strftime("%d-%m-%Y"),
                "SNo": i,
                "Narration": narration,
                "Debit": 0,
                "Credit": salary_credit,
                "Balance": round(balance + salary_credit, 2)
            })
            balance += salary_credit
            continue

        # Create a transaction description with unique details
        unique_details = f"Ref No: {random.randint(100000, 999999)}"
        description = f"{narration} ({unique_details})"

        transaction = {
            "Date": transaction_date.strftime("%d-%m-%Y"),
            "SNo": i,
            "Narration": description,
            "Debit": debit,
            "Credit": credit,
            "Balance": round(balance, 2)
        }
        statement.append(transaction)

    return statement

# Create a DataFrame and save it as a CSV
df = pd.DataFrame(generate_statement())
df.to_csv("synthetic_bank_statement_realistic_v4.csv", index=False)

print("Realistic synthetic bank statement generated and saved as 'synthetic_bank_statement_realistic_v4.csv'.")