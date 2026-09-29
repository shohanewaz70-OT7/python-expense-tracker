
import json
import os
from datetime import datetime


# -----------------------------
# File names
# -----------------------------

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budget.json"


# -----------------------------
# Categories
# -----------------------------

CATEGORIES = {
    "1": "Food",
    "2": "Transport",
    "3": "Shopping",
    "4": "Education",
    "5": "Other"
}


# -----------------------------
# Load and save functions
# -----------------------------

def load_expenses():
    """Load expenses from the JSON file."""

    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)

    return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""

    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def load_budget():
    """Load the saved monthly budget."""

    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as file:
            budget_data = json.load(file)
            return budget_data.get("monthly_budget", 0)

    return 0


def save_budget(monthly_budget):
    """Save the monthly budget."""

    budget_data = {
        "monthly_budget": monthly_budget
    }

    with open(BUDGET_FILE, "w") as file:
        json.dump(budget_data, file, indent=4)


# -----------------------------
# Expense functions
# -----------------------------

def add_expense(expenses):
    """Add a new expense."""

    expense = input("\nWhat did you spend money on? ").strip()

    if not expense:
        print("\nItem name cannot be empty.")
        return

    try:
        amount = float(input("How much did you spend? "))

        if amount <= 0:
            print("\nAmount must be greater than zero.")
            return

    except ValueError:
        print("\nPlease enter a valid amount.")
        return

    print("\nChoose a category:")

    for number, category in CATEGORIES.items():
        print(f"{number}. {category}")

    category_choice = input("Enter the category number: ")

    category = CATEGORIES.get(category_choice, "Other")

    expense_data = {
        "item": expense,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(expense_data)
    save_expenses(expenses)

    print("\nExpense added successfully!")


def view_expenses(expenses):
    """Display all recorded expenses."""

    print("\nYour Expenses:")
    print("-" * 50)

    if not expenses:
        print("No expenses recorded yet.")
        return

    for number, item in enumerate(expenses, start=1):
        print(
            f"{number}. {item['item']} - "
            f"{item['amount']:.2f} BDT - "
            f"{item['category']} - "
            f"{item.get('date', 'Unknown date')}"
        )


def delete_expense(expenses):
    """Delete an expense."""

    if not expenses:
        print("\nThere are no expenses to delete.")
        return

    view_expenses(expenses)

    try:
        number = int(
            input("\nEnter the expense number to delete: ")
        )

        if 1 <= number <= len(expenses):
            deleted = expenses.pop(number - 1)

            save_expenses(expenses)

            print(f"\nDeleted: {deleted['item']}")

        else:
            print("\nInvalid expense number.")

    except ValueError:
        print("\nPlease enter a valid number.")


def edit_expense(expenses):
    """Edit an existing expense."""

    if not expenses:
        print("\nThere are no expenses to edit.")
        return

    view_expenses(expenses)

    try:
        number = int(
            input("\nEnter the expense number to edit: ")
        )

        if not (1 <= number <= len(expenses)):
            print("\nInvalid expense number.")
            return

    except ValueError:
        print("\nPlease enter a valid number.")
        return

    selected = expenses[number - 1]

    print("\nWhat would you like to change?")
    print("1. Item")
    print("2. Amount")
    print("3. Category")

    edit_choice = input("Enter your choice: ")

    if edit_choice == "1":
        new_item = input("Enter the new item name: ").strip()

        if not new_item:
            print("\nItem name cannot be empty.")
            return

        selected["item"] = new_item

    elif edit_choice == "2":
        try:
            new_amount = float(
                input("Enter the new amount: ")
            )

            if new_amount <= 0:
                print("\nAmount must be greater than zero.")
                return

            selected["amount"] = new_amount

        except ValueError:
            print("\nPlease enter a valid amount.")
            return

    elif edit_choice == "3":
        print("\nChoose a new category:")

        for number, category in CATEGORIES.items():
            print(f"{number}. {category}")

        new_category = input(
            "Enter the category number: "
        )

        selected["category"] = CATEGORIES.get(
            new_category,
            "Other"
        )

    else:
        print("\nInvalid choice.")
        return

    save_expenses(expenses)

    print("\nExpense updated successfully!")


# -----------------------------
# Spending functions
# -----------------------------

def show_total_spending(expenses):
    """Show total spending."""

    total_spent = sum(
        item["amount"]
        for item in expenses
    )

    current_month = datetime.now().strftime("%Y-%m")

    monthly_spending = sum(
        item["amount"]
        for item in expenses
        if item.get("date", "").startswith(current_month)
    )

    print(f"\nTotal Spent: {total_spent:.2f} BDT")
    print(
        f"Current Month Spending: "
        f"{monthly_spending:.2f} BDT"
    )


def category_summary(expenses):
    """Show spending for each category."""

    print("\nSpending by Category:")
    print("-" * 35)

    for category in CATEGORIES.values():

        category_total = sum(
            item["amount"]
            for item in expenses
            if item["category"] == category
        )

        print(
            f"{category}: "
            f"{category_total:.2f} BDT"
        )


# -----------------------------
# Budget functions
# -----------------------------

def get_monthly_spending(expenses):
    """Calculate spending for the current month."""

    current_month = datetime.now().strftime("%Y-%m")

    return sum(
        item["amount"]
        for item in expenses
        if item.get("date", "").startswith(current_month)
    )


def show_budget_status(expenses, monthly_budget):
    """Display the current budget status."""

    monthly_spending = get_monthly_spending(expenses)

    print("\n" + "=" * 35)
    print("        MONTHLY BUDGET STATUS")
    print("=" * 35)

    if monthly_budget <= 0:
        print("No monthly budget has been set.")
        print("Choose option 7 to set your budget.")
        return

    print(
        f"Monthly Budget: "
        f"{monthly_budget:.2f} BDT"
    )

    print(
        f"Spent This Month: "
        f"{monthly_spending:.2f} BDT"
    )

    remaining = monthly_budget - monthly_spending

    if monthly_spending < monthly_budget:

        print(
            f"Remaining Budget: "
            f"{remaining:.2f} BDT"
        )

        percentage = (
            monthly_spending /
            monthly_budget
        ) * 100

        print(
            f"Budget Used: "
            f"{percentage:.1f}%"
        )

        if percentage >= 80:
            print(
                "\nWarning: You have used "
                "80% or more of your budget!"
            )

    elif monthly_spending == monthly_budget:

        print("Remaining Budget: 0.00 BDT")

        print(
            "\nWarning: You have reached "
            "your monthly budget!"
        )

    else:

        exceeded = (
            monthly_spending -
            monthly_budget
        )

        print(
            f"Budget Exceeded By: "
            f"{exceeded:.2f} BDT"
        )

        print(
            "\nWarning: You have exceeded "
            "your monthly budget!"
        )


def set_monthly_budget():
    """Set a new monthly budget."""

    try:
        new_budget = float(
            input(
                "\nEnter your monthly budget in BDT: "
            )
        )

        if new_budget <= 0:
            print(
                "\nBudget must be greater than zero."
            )

            return None

        save_budget(new_budget)

        print(
            f"\nMonthly budget saved: "
            f"{new_budget:.2f} BDT"
        )

        return new_budget

    except ValueError:
        print("\nPlease enter a valid budget amount.")

        return None


# -----------------------------
# Monthly report
# -----------------------------

def monthly_report(expenses):
    """Generate a report for a selected month."""

    print("\n" + "=" * 35)
    print("        MONTHLY EXPENSE REPORT")
    print("=" * 35)

    report_month = input(
        "Enter month (YYYY-MM), "
        "or press Enter for current month: "
    ).strip()

    if report_month == "":
        report_month = datetime.now().strftime("%Y-%m")

    try:
        datetime.strptime(
            report_month,
            "%Y-%m"
        )

    except ValueError:
        print(
            "\nInvalid month format. "
            "Use YYYY-MM, for example 2026-09."
        )

        return

    month_expenses = [
        item
        for item in expenses
        if item.get("date", "").startswith(
            report_month
        )
    ]

    if not month_expenses:
        print(
            f"\nNo expenses recorded "
            f"for {report_month}."
        )

        return

    total = sum(
        item["amount"]
        for item in month_expenses
    )

    transaction_count = len(month_expenses)

    print(f"\nReport Month: {report_month}")

    print(
        f"Total Spending: "
        f"{total:.2f} BDT"
    )

    print(
        f"Number of Transactions: "
        f"{transaction_count}"
    )

    # Category totals
    category_totals = {}

    for item in month_expenses:

        category = item["category"]
        amount = item["amount"]

        category_totals[category] = (
            category_totals.get(category, 0)
            + amount
        )

    print("\nSpending by Category:")
    print("-" * 35)

    for category, amount in category_totals.items():

        print(
            f"{category}: "
            f"{amount:.2f} BDT"
        )

    # Highest spending category
    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    print(
        f"\nHighest Spending Category: "
        f"{highest_category} "
        f"({category_totals[highest_category]:.2f} BDT)"
    )

    # Previous month
    year, month = map(
        int,
        report_month.split("-")
    )

    if month == 1:
        previous_month = f"{year - 1}-12"
    else:
        previous_month = (
            f"{year}-{month - 1:02d}"
        )

    previous_expenses = [
        item
        for item in expenses
        if item.get("date", "").startswith(
            previous_month
        )
    ]

    previous_total = sum(
        item["amount"]
        for item in previous_expenses
    )

    print("\nComparison with Previous Month:")

    print(
        f"Previous Month ({previous_month}): "
        f"{previous_total:.2f} BDT"
    )

    print(
        f"Selected Month ({report_month}): "
        f"{total:.2f} BDT"
    )

    difference = total - previous_total

    if previous_total == 0:

        print(
            "No previous-month spending "
            "available for comparison."
        )

    elif difference > 0:

        print(
            f"Spending increased by "
            f"{difference:.2f} BDT."
        )

    elif difference < 0:

        print(
            f"Spending decreased by "
            f"{abs(difference):.2f} BDT."
        )

    else:

        print("Spending remained the same.")


# -----------------------------
# Main program
# -----------------------------

def main():

    print("Welcome to My Expense Tracker!")

    expenses = load_expenses()
    monthly_budget = load_budget()

    while True:

        print("\n" + "=" * 35)
        print("       EXPENSE TRACKER")
        print("=" * 35)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spending")
        print("4. Category Summary")
        print("5. Delete Expense")
        print("6. Edit Expense")
        print("7. Set Monthly Budget")
        print("8. View Budget Status")
        print("9. Monthly Expense Report")
        print("10. Exit")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            add_expense(expenses)

            if monthly_budget > 0:
                show_budget_status(
                    expenses,
                    monthly_budget
                )

        elif choice == "2":

            view_expenses(expenses)

        elif choice == "3":

            show_total_spending(expenses)

        elif choice == "4":

            category_summary(expenses)

        elif choice == "5":

            delete_expense(expenses)

        elif choice == "6":

            edit_expense(expenses)

        elif choice == "7":

            new_budget = set_monthly_budget()

            if new_budget is not None:
                monthly_budget = new_budget

        elif choice == "8":

            show_budget_status(
                expenses,
                monthly_budget
            )

        elif choice == "9":

            monthly_report(expenses)

        elif choice == "10":

            print(
                "\nThank you for using "
                "Expense Tracker!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-10."
            )


# Start the program
if __name__ == "__main__":
    main()