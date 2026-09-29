# Python Expense Tracker

A desktop expense tracking application built with **Python and Tkinter**. The application allows users to record, manage, analyze, and monitor their expenses through a graphical user interface.

## Features

* Add, edit, and delete expenses
* Automatic date recording
* Expense categories
* Persistent data storage using JSON
* Search expenses by item
* Filter expenses by category
* Filter expenses by month
* Calculate total spending
* Monthly spending analysis
* Monthly budget management
* Budget progress dashboard
* Category spending visualization with a pie chart
* Monthly expense reports
* Previous-month spending comparison
* Scrollable graphical interface

## Technologies Used

* Python
* Tkinter
* JSON
* Matplotlib
* UUID
* Datetime

## Project Structure

```text
python-expense-tracker/
│
├── expense_tracker.py
├── expense_tracker_gui.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/python-expense-tracker.git
cd python-expense-tracker
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

## How to Run

Run the graphical application with:

```bash
python expense_tracker_gui.py
```

The application will create and use local JSON files for storing expenses and budget information.

## Main Interface

The application provides a graphical interface for entering expenses, viewing transactions, managing a monthly budget, and analyzing spending.

## What I Learned

Through this project, I practiced:

* Python functions and program structure
* Lists and dictionaries
* File handling
* JSON data persistence
* Exception handling
* Object/event-based GUI programming with Tkinter
* Working with external Python libraries
* Data visualization with Matplotlib
* Filtering and analyzing data
* Designing a complete small-scale desktop application

## Future Improvements

Possible future improvements include:

* Exporting reports to CSV or PDF
* Adding more advanced data visualization
* Adding recurring expenses
* Adding income tracking
* Adding a database instead of JSON storage
* Adding user accounts and authentication

## Author

Built as a Python portfolio project.
