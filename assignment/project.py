import csv
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.csv"
BUDGET_FILE = "budget.txt"

expenses = []
monthly_budget = 0.0


# Load saved expenses when the program starts
def load_expenses():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row["amount"] = float(row["amount"])
                    expenses.append(row)

            print("Previous expenses loaded successfully.")

        except (ValueError, KeyError, csv.Error):
            print("Some saved expense data could not be loaded.")
        except OSError:
            print("Unable to read the expenses file.")


# Save expenses to a CSV file
def save_expenses():
    try:
        with open(FILE_NAME, "w", newline="") as file:
            fieldnames = ["amount", "category", "date", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(expenses)

        print("Expenses saved successfully.")

    except OSError:
        print("Unable to save expenses.")


# Load the monthly budget
def load_budget():
    global monthly_budget

    try:
        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, "r") as file:
                monthly_budget = float(file.read())

    except (ValueError, OSError):
        monthly_budget = 0.0


# Set and save the monthly budget
def set_budget():
    global monthly_budget

    try:
        amount = float(input("Enter monthly budget (₦): "))

        if amount <= 0:
            print("Budget must be greater than zero.")
            return

        monthly_budget = amount

        with open(BUDGET_FILE, "w") as file:
            file.write(str(monthly_budget))

        print(f"Monthly budget set to ₦{monthly_budget:,.2f}")

        check_budget()

    except ValueError:
        print("Please enter a valid number.")
    except OSError:
        print("Unable to save the budget.")


# Get expenses for a particular month
def get_month_expenses(month):
    return [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]


# Add a new expense
def add_expense():
    try:
        amount = float(input("Enter amount spent (₦): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        category = input(
            "Category (food, transport, data, rent, etc.): "
        ).strip().title()

        if not category:
            print("Category cannot be empty.")
            return

        date_text = input("Enter date (YYYY-MM-DD): ").strip()

        # Check whether the date is valid
        datetime.strptime(date_text, "%Y-%m-%d")

        description = input("What did you spend on? ").strip()

        expense = {
            "amount": amount,
            "category": category,
            "date": date_text,
            "description": description
        }

        expenses.append(expense)
        save_expenses()

        print("Expense added successfully!")
        check_budget()

    except ValueError:
        print("Invalid amount or date. Please try again.")


# View all expenses
def view_expenses(records=None):
    if records is None:
        records = expenses

    if not records:
        print("No expenses found.")
        return

    print("\n--- EXPENSE RECORDS ---")

    for number, expense in enumerate(records, start=1):
        print(
            f"{number}. {expense['date']} | "
            f"{expense['category']} | "
            f"₦{expense['amount']:,.2f} | "
            f"{expense['description']}"
        )


# Calculate total spending
def show_total():
    total = sum(expense["amount"] for expense in expenses)

    print(f"Total spent: ₦{total:,.2f}")


# Calculate spending for each category
def show_category_totals(records=None):
    if records is None:
        records = expenses

    if not records:
        print("No expenses found.")
        return

    totals = defaultdict(float)

    for expense in records:
        totals[expense["category"]] += expense["amount"]

    print("\n--- SPENDING BY CATEGORY ---")

    for category, amount in sorted(totals.items()):
        print(f"{category}: ₦{amount:,.2f}")


# Warn when monthly spending reaches 80% of budget
def check_budget():
    if monthly_budget <= 0:
        return

    current_month = datetime.today().strftime("%Y-%m")
    records = get_month_expenses(current_month)

    total = sum(expense["amount"] for expense in records)
    percentage = (total / monthly_budget) * 100

    print(
        f"Monthly spending: ₦{total:,.2f} "
        f"of ₦{monthly_budget:,.2f} "
        f"({percentage:.1f}%)"
    )

    if percentage >= 100:
        print("WARNING: Your monthly budget has been exceeded!")
    elif percentage >= 80:
        print("Warning: You have used at least 80% of your budget.")


# Find the category with the highest spending
def show_highest_category(records=None):
    if records is None:
        records = expenses

    totals = defaultdict(float)

    for expense in records:
        totals[expense["category"]] += expense["amount"]

    if not totals:
        print("No expenses found.")
        return

    category = max(totals, key=totals.get)

    print(
        f"Highest spending category: {category} "
        f"(₦{totals[category]:,.2f})"
    )


# Filter expenses by month
def filter_by_month():
    month = input(
        "Enter month (YYYY-MM), e.g. 2026-10: "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    records = get_month_expenses(month)

    if not records:
        print("No expenses found for this month.")
        return

    view_expenses(records)

    total = sum(expense["amount"] for expense in records)
    print(f"Total for {month}: ₦{total:,.2f}")

    show_category_totals(records)


# Main menu
def main():
    load_expenses()
    load_budget()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. Show total spent")
        print("4. Show spending by category")
        print("5. Set monthly budget")
        print("6. Show highest spending category")
        print("7. Filter expenses by month")
        print("8. Save and exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            show_category_totals()
        elif choice == "5":
            set_budget()
        elif choice == "6":
            show_highest_category()
        elif choice == "7":
            filter_by_month()
        elif choice == "8":
            save_expenses()
            print("Thank you for using the tracker!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
