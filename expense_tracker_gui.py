import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import uuid

import matplotlib.pyplot as plt


# ============================================================
# FILES & CONSTANTS
# ============================================================

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Education",
    "Other"
]


# ============================================================
# DATA FUNCTIONS
# ============================================================

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, "r") as file:
                data = json.load(file)

                changed = False

                for item in data:
                    if "id" not in item:
                        item["id"] = str(uuid.uuid4())
                        changed = True

                if changed:
                    save_expenses(data)

                return data

        except (json.JSONDecodeError, OSError):
            messagebox.showerror(
                "File Error",
                "Could not read expenses.json."
            )

    return []


def save_expenses(expenses_data):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses_data, file, indent=4)


def load_budget():
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as file:
                data = json.load(file)
                return data.get("monthly_budget", 0)

        except (json.JSONDecodeError, OSError):
            return 0

    return 0


def save_budget(budget):
    with open(BUDGET_FILE, "w") as file:
        json.dump(
            {"monthly_budget": budget},
            file,
            indent=4
        )


# ============================================================
# CALCULATIONS
# ============================================================

def get_current_month():
    return datetime.now().strftime("%Y-%m")


def get_monthly_spending():
    current_month = get_current_month()

    return sum(
        item["amount"]
        for item in expenses
        if item.get("date", "").startswith(current_month)
    )


def update_total():
    total = sum(
        item["amount"]
        for item in expenses
    )

    total_label.config(
        text=f"Total Spending\n{total:,.2f} BDT"
    )


def update_budget_dashboard():
    monthly_spending = get_monthly_spending()

    budget_label.config(
        text=f"Budget: {monthly_budget:,.2f} BDT"
    )

    spent_label.config(
        text=f"Spent: {monthly_spending:,.2f} BDT"
    )

    if monthly_budget <= 0:

        remaining_label.config(
            text="Remaining: No budget set"
        )

        percentage_label.config(
            text="Budget Used: 0%"
        )

        budget_progress["value"] = 0

        return

    remaining = monthly_budget - monthly_spending

    percentage = (
        monthly_spending / monthly_budget
    ) * 100

    budget_progress["value"] = min(
        percentage,
        100
    )

    percentage_label.config(
        text=f"Budget Used: {percentage:.1f}%"
    )

    if remaining >= 0:

        remaining_label.config(
            text=f"Remaining: {remaining:,.2f} BDT"
        )

    else:

        remaining_label.config(
            text=f"Exceeded By: {abs(remaining):,.2f} BDT"
        )


# ============================================================
# TABLE
# ============================================================

def display_expenses(expense_data=None):

    if expense_data is None:
        expense_data = expenses

    for row in expense_table.get_children():
        expense_table.delete(row)

    for number, item in enumerate(
        expense_data,
        start=1
    ):

        expense_table.insert(
            "",
            tk.END,
            iid=item["id"],
            values=(
                number,
                item["item"],
                f"{item['amount']:,.2f}",
                item["category"],
                item.get("date", "Unknown")
            )
        )


# ============================================================
# INPUT MANAGEMENT
# ============================================================

def clear_fields():

    item_entry.delete(
        0,
        tk.END
    )

    amount_entry.delete(
        0,
        tk.END
    )

    category_var.set(
        "Food"
    )

    item_entry.focus()


# ============================================================
# ADD EXPENSE
# ============================================================

def add_expense():

    item = item_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_var.get()

    if not item or not amount:

        messagebox.showerror(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    try:

        amount = float(amount)

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Amount must be greater than zero."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return

    expense = {
        "id": str(uuid.uuid4()),
        "item": item,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(
        expense
    )

    save_expenses(
        expenses
    )

    display_expenses()

    update_total()

    update_budget_dashboard()

    clear_fields()


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_expense():

    selected = expense_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to delete."
        )

        return

    expense_id = selected[0]

    selected_expense = next(
        (
            item
            for item in expenses
            if item["id"] == expense_id
        ),
        None
    )

    if selected_expense is None:
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete '{selected_expense['item']}'?"
    )

    if not confirm:
        return

    expenses.remove(
        selected_expense
    )

    save_expenses(
        expenses
    )

    display_expenses()

    update_total()

    update_budget_dashboard()


# ============================================================
# EDIT EXPENSE
# ============================================================

def edit_expense():

    selected = expense_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to edit."
        )

        return

    expense_id = selected[0]

    selected_expense = next(
        (
            item
            for item in expenses
            if item["id"] == expense_id
        ),
        None
    )

    if selected_expense is None:
        return

    item_entry.delete(
        0,
        tk.END
    )

    item_entry.insert(
        0,
        selected_expense["item"]
    )

    amount_entry.delete(
        0,
        tk.END
    )

    amount_entry.insert(
        0,
        str(selected_expense["amount"])
    )

    category_var.set(
        selected_expense["category"]
    )

    add_button.config(
        text="Update Expense",
        command=lambda: update_expense(
            selected_expense
        )
    )


def update_expense(selected_expense):

    item = item_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_var.get()

    if not item or not amount:

        messagebox.showerror(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    try:

        amount = float(amount)

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Amount must be greater than zero."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return

    selected_expense["item"] = item
    selected_expense["amount"] = amount
    selected_expense["category"] = category

    save_expenses(
        expenses
    )

    display_expenses()

    update_total()

    update_budget_dashboard()

    clear_fields()

    add_button.config(
        text="Add Expense",
        command=add_expense
    )


# ============================================================
# BUDGET
# ============================================================

def set_budget():

    global monthly_budget

    budget_window = tk.Toplevel(
        window
    )

    budget_window.title(
        "Set Monthly Budget"
    )

    budget_window.geometry(
        "380x220"
    )

    budget_window.resizable(
        False,
        False
    )

    tk.Label(
        budget_window,
        text="Monthly Budget",
        font=("Arial", 16, "bold")
    ).pack(
        pady=20
    )

    tk.Label(
        budget_window,
        text="Enter your budget in BDT:"
    ).pack()

    budget_entry = tk.Entry(
        budget_window,
        width=25
    )

    budget_entry.pack(
        pady=10
    )

    budget_entry.insert(
        0,
        str(monthly_budget)
    )

    def save_new_budget():

        global monthly_budget

        try:

            new_budget = float(
                budget_entry.get()
            )

            if new_budget <= 0:

                messagebox.showerror(
                    "Invalid Budget",
                    "Budget must be greater than zero.",
                    parent=budget_window
                )

                return

            monthly_budget = new_budget

            save_budget(
                monthly_budget
            )

            update_budget_dashboard()

            budget_window.destroy()

        except ValueError:

            messagebox.showerror(
                "Invalid Budget",
                "Please enter a valid number.",
                parent=budget_window
            )

    tk.Button(
        budget_window,
        text="Save Budget",
        width=18,
        command=save_new_budget
    ).pack(
        pady=15
    )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

def show_category_analysis():

    category_totals = {}

    for item in expenses:

        category = item["category"]

        category_totals[category] = (
            category_totals.get(
                category,
                0
            )
            + item["amount"]
        )

    if not category_totals:

        messagebox.showinfo(
            "Category Analysis",
            "No expenses available."
        )

        return

    labels = list(
        category_totals.keys()
    )

    values = list(
        category_totals.values()
    )

    plt.figure(
        figsize=(7, 7)
    )

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    plt.title(
        "Spending by Category"
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MONTHLY REPORT
# ============================================================

def show_monthly_report():

    report_window = tk.Toplevel(
        window
    )

    report_window.title(
        "Monthly Expense Report"
    )

    report_window.geometry(
        "600x600"
    )

    tk.Label(
        report_window,
        text="MONTHLY EXPENSE REPORT",
        font=("Arial", 20, "bold")
    ).pack(
        pady=20
    )

    tk.Label(
        report_window,
        text="Enter month (YYYY-MM):"
    ).pack()

    month_entry = tk.Entry(
        report_window,
        width=20
    )

    month_entry.pack(
        pady=5
    )

    month_entry.insert(
        0,
        get_current_month()
    )

    report_text = tk.Text(
        report_window,
        width=65,
        height=22
    )

    report_text.pack(
        padx=20,
        pady=15
    )

    def generate_report():

        month = month_entry.get().strip()

        try:

            datetime.strptime(
                month,
                "%Y-%m"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Month",
                "Use YYYY-MM format, for example 2026-09.",
                parent=report_window
            )

            return

        month_expenses = [
            item
            for item in expenses
            if item.get(
                "date",
                ""
            ).startswith(month)
        ]

        report_text.delete(
            "1.0",
            tk.END
        )

        if not month_expenses:

            report_text.insert(
                tk.END,
                f"No expenses found for {month}."
            )

            return

        total = sum(
            item["amount"]
            for item in month_expenses
        )

        transaction_count = len(
            month_expenses
        )

        category_totals = {}

        for item in month_expenses:

            category = item["category"]

            category_totals[category] = (
                category_totals.get(
                    category,
                    0
                )
                + item["amount"]
            )

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        year, month_number = map(
            int,
            month.split("-")
        )

        if month_number == 1:

            previous_month = (
                f"{year - 1}-12"
            )

        else:

            previous_month = (
                f"{year}-"
                f"{month_number - 1:02d}"
            )

        previous_total = sum(
            item["amount"]
            for item in expenses
            if item.get(
                "date",
                ""
            ).startswith(
                previous_month
            )
        )

        report = (
            f"Report Month: {month}\n"
            f"{'=' * 45}\n\n"
            f"Total Spending: "
            f"{total:,.2f} BDT\n\n"
            f"Transactions: "
            f"{transaction_count}\n\n"
            f"Spending by Category:\n"
            f"{'-' * 30}\n"
        )

        for category, amount in category_totals.items():

            report += (
                f"{category}: "
                f"{amount:,.2f} BDT\n"
            )

        report += (
            f"\nHighest Spending Category:\n"
            f"{highest_category} "
            f"({category_totals[highest_category]:,.2f} BDT)\n\n"
            f"Previous Month ({previous_month}): "
            f"{previous_total:,.2f} BDT\n"
            f"Selected Month ({month}): "
            f"{total:,.2f} BDT\n"
        )

        difference = (
            total - previous_total
        )

        if previous_total == 0:

            report += (
                "\nNo previous-month "
                "spending available."
            )

        elif difference > 0:

            report += (
                f"\nSpending increased by "
                f"{difference:,.2f} BDT."
            )

        elif difference < 0:

            report += (
                f"\nSpending decreased by "
                f"{abs(difference):,.2f} BDT."
            )

        else:

            report += (
                "\nSpending remained the same."
            )

        report_text.insert(
            tk.END,
            report
        )

    tk.Button(
        report_window,
        text="Generate Report",
        width=20,
        command=generate_report
    ).pack(
        pady=5
    )


# ============================================================
# SEARCH & FILTER
# ============================================================

def apply_filter():

    search_text = (
        search_entry
        .get()
        .strip()
        .lower()
    )

    selected_category = (
        filter_category_var.get()
    )

    selected_month = (
        month_filter_entry
        .get()
        .strip()
    )

    filtered = []

    for item in expenses:

        matches_search = (
            search_text == ""
            or search_text
            in item["item"].lower()
        )

        matches_category = (
            selected_category == "All"
            or item["category"]
            == selected_category
        )

        matches_month = (
            selected_month == ""
            or item.get(
                "date",
                ""
            ).startswith(
                selected_month
            )
        )

        if (
            matches_search
            and matches_category
            and matches_month
        ):

            filtered.append(item)

    display_expenses(
        filtered
    )


def clear_filter():

    search_entry.delete(
        0,
        tk.END
    )

    filter_category_var.set(
        "All"
    )

    month_filter_entry.delete(
        0,
        tk.END
    )

    display_expenses()


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Expense Tracker"
)

window.geometry(
    "1050x650"
)

window.minsize(
    750,
    500
)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use(
        "clam"
    )
except tk.TclError:
    pass

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

style.configure(
    "Horizontal.TProgressbar",
    thickness=15
)


# ============================================================
# LOAD DATA
# ============================================================

expenses = load_expenses()

monthly_budget = load_budget()


# ============================================================
# SCROLLABLE MAIN AREA
# ============================================================

outer_frame = tk.Frame(
    window
)

outer_frame.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    outer_frame,
    highlightthickness=0
)

vertical_scrollbar = ttk.Scrollbar(
    outer_frame,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=vertical_scrollbar.set
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


main_frame = tk.Frame(
    canvas
)

canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_main_frame(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_main_frame
)


# Mouse wheel scrolling

def mouse_wheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    main_frame,
    text="EXPENSE TRACKER",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=(12, 2)
)

subtitle = tk.Label(
    main_frame,
    text="Track your spending • Manage your budget • Understand your habits",
    font=("Arial", 10)
)

subtitle.pack(
    pady=(0, 8)
)


# ============================================================
# DASHBOARD
# ============================================================

dashboard = tk.LabelFrame(
    main_frame,
    text="Monthly Budget Dashboard",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=7
)

dashboard.pack(
    fill="x",
    padx=20,
    pady=5
)

dashboard_info = tk.Frame(
    dashboard
)

dashboard_info.pack()


budget_label = tk.Label(
    dashboard_info,
    text="Budget: 0.00 BDT",
    font=("Arial", 10, "bold")
)

budget_label.grid(
    row=0,
    column=0,
    padx=18
)


spent_label = tk.Label(
    dashboard_info,
    text="Spent: 0.00 BDT",
    font=("Arial", 10, "bold")
)

spent_label.grid(
    row=0,
    column=1,
    padx=18
)


remaining_label = tk.Label(
    dashboard_info,
    text="Remaining: No budget set",
    font=("Arial", 10, "bold")
)

remaining_label.grid(
    row=0,
    column=2,
    padx=18
)


percentage_label = tk.Label(
    dashboard_info,
    text="Budget Used: 0%",
    font=("Arial", 10, "bold")
)

percentage_label.grid(
    row=0,
    column=3,
    padx=18
)


budget_progress = ttk.Progressbar(
    dashboard,
    length=600,
    mode="determinate"
)

budget_progress.pack(
    pady=6
)


tk.Button(
    dashboard,
    text="Set Monthly Budget",
    width=18,
    command=set_budget
).pack()


# ============================================================
# INPUT AREA
# ============================================================

input_frame = tk.LabelFrame(
    main_frame,
    text="Add / Edit Expense",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=7
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=5
)


tk.Label(
    input_frame,
    text="Expense Item:"
).grid(
    row=0,
    column=0,
    padx=6
)

item_entry = tk.Entry(
    input_frame,
    width=25
)

item_entry.grid(
    row=1,
    column=0,
    padx=6
)


tk.Label(
    input_frame,
    text="Amount (BDT):"
).grid(
    row=0,
    column=1,
    padx=6
)

amount_entry = tk.Entry(
    input_frame,
    width=18
)

amount_entry.grid(
    row=1,
    column=1,
    padx=6
)


tk.Label(
    input_frame,
    text="Category:"
).grid(
    row=0,
    column=2,
    padx=6
)


category_var = tk.StringVar()

category_dropdown = ttk.Combobox(
    input_frame,
    textvariable=category_var,
    values=CATEGORIES,
    state="readonly",
    width=16
)

category_dropdown.grid(
    row=1,
    column=2,
    padx=6
)

category_dropdown.set(
    "Food"
)


add_button = tk.Button(
    input_frame,
    text="Add Expense",
    width=18,
    command=add_expense
)

add_button.grid(
    row=1,
    column=3,
    padx=12
)


# ============================================================
# TOTAL
# ============================================================

total_label = tk.Label(
    main_frame,
    text="Total Spending\n0.00 BDT",
    font=("Arial", 16, "bold")
)

total_label.pack(
    pady=5
)


# ============================================================
# SEARCH & FILTER
# ============================================================

filter_frame = tk.LabelFrame(
    main_frame,
    text="Search & Filter",
    font=("Arial", 10, "bold"),
    padx=8,
    pady=6
)

filter_frame.pack(
    fill="x",
    padx=20,
    pady=3
)


tk.Label(
    filter_frame,
    text="Search:"
).grid(
    row=0,
    column=0,
    padx=4
)

search_entry = tk.Entry(
    filter_frame,
    width=18
)

search_entry.grid(
    row=1,
    column=0,
    padx=4
)


tk.Label(
    filter_frame,
    text="Category:"
).grid(
    row=0,
    column=1,
    padx=4
)


filter_category_var = tk.StringVar()

filter_category_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=filter_category_var,
    values=["All"] + CATEGORIES,
    state="readonly",
    width=13
)

filter_category_dropdown.grid(
    row=1,
    column=1,
    padx=4
)

filter_category_dropdown.set(
    "All"
)


tk.Label(
    filter_frame,
    text="Month (YYYY-MM):"
).grid(
    row=0,
    column=2,
    padx=4
)


month_filter_entry = tk.Entry(
    filter_frame,
    width=14
)

month_filter_entry.grid(
    row=1,
    column=2,
    padx=4
)


tk.Button(
    filter_frame,
    text="Apply Filter",
    width=13,
    command=apply_filter
).grid(
    row=1,
    column=3,
    padx=6
)


tk.Button(
    filter_frame,
    text="Clear",
    width=9,
    command=clear_filter
).grid(
    row=1,
    column=4,
    padx=4
)


# ============================================================
# EXPENSE HISTORY
# ============================================================

tk.Label(
    main_frame,
    text="Expense History",
    font=("Arial", 13, "bold")
).pack(
    pady=3
)


table_frame = tk.Frame(
    main_frame
)

table_frame.pack(
    fill="both",
    padx=20
)


expense_table = ttk.Treeview(
    table_frame,
    columns=(
        "Number",
        "Item",
        "Amount",
        "Category",
        "Date"
    ),
    show="headings",
    height=8
)


expense_table.heading(
    "Number",
    text="#"
)

expense_table.heading(
    "Item",
    text="Item"
)

expense_table.heading(
    "Amount",
    text="Amount (BDT)"
)

expense_table.heading(
    "Category",
    text="Category"
)

expense_table.heading(
    "Date",
    text="Date"
)


expense_table.column(
    "Number",
    width=45,
    anchor="center"
)

expense_table.column(
    "Item",
    width=280
)

expense_table.column(
    "Amount",
    width=125,
    anchor="center"
)

expense_table.column(
    "Category",
    width=145,
    anchor="center"
)

expense_table.column(
    "Date",
    width=120,
    anchor="center"
)


table_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=expense_table.yview
)

expense_table.configure(
    yscrollcommand=table_scrollbar.set
)


expense_table.pack(
    side="left",
    fill="x",
    expand=True
)

table_scrollbar.pack(
    side="right",
    fill="y"
)


# ============================================================
# EDIT / DELETE
# ============================================================

button_frame = tk.Frame(
    main_frame
)

button_frame.pack(
    pady=6
)


tk.Button(
    button_frame,
    text="Edit Selected",
    width=16,
    command=edit_expense
).grid(
    row=0,
    column=0,
    padx=8
)


tk.Button(
    button_frame,
    text="Delete Selected",
    width=16,
    command=delete_expense
).grid(
    row=0,
    column=1,
    padx=8
)


# ============================================================
# ANALYTICS
# ============================================================

analytics_frame = tk.Frame(
    main_frame
)

analytics_frame.pack(
    pady=(0, 12)
)


tk.Button(
    analytics_frame,
    text="Spending by Category",
    width=20,
    command=show_category_analysis
).grid(
    row=0,
    column=0,
    padx=8
)


tk.Button(
    analytics_frame,
    text="Monthly Report",
    width=20,
    command=show_monthly_report
).grid(
    row=0,
    column=1,
    padx=8
)


# ============================================================
# START APPLICATION
# ============================================================

display_expenses()

update_total()

update_budget_dashboard()

item_entry.focus()

window.mainloop()