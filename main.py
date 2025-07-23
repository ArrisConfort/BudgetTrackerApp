## Budget Tracker Application# This application allows users to track their monthly income and expenses.
# It provides functionalities to add transactions, view summaries, and categorize expenses.
# The data is stored in a CSV file for persistence.

import csv
from datetime import datetime
from collections import defaultdict

class Transaction:
    def __init__(self, amount, category, transactionType, date=None):
        self.amount = float(amount)
        self.category = category
        self.transactionType = transactionType  # 'Income' or 'Expense'
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def toList(self):
        return [self.date, self.transactionType, self.category, f"{self.amount:.2f}"]


class BudgetTracker:
    def __init__(self, filename='transactions.csv'):
        self.filename = filename
        self.transactions = []
        self.loadTransactions()

    def addTransaction(self, transaction):
        self.transactions.append(transaction)
        self.saveTransaction(transaction)

    def saveTransaction(self, transaction):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(transaction.toList())

    def loadTransactions(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4 and row[0] != 'Date':
                        date, tType, category, amount = row
                        self.transactions.append(Transaction(amount, category, tType, date))
        except FileNotFoundError:
            pass  # Start with empty transactions if file doesn't exist

    def viewSummary(self):
        income = sum(t.amount for t in self.transactions if t.transactionType == 'Income')
        expense = sum(t.amount for t in self.transactions if t.transactionType == 'Expense')
        balance = income - expense
        print(f"\nSummary:")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expenses: ${expense:.2f}")
        print(f"Net Balance: ${balance:.2f}")

    def viewByCategory(self):
        categorySummary = defaultdict(float)
        for t in self.transactions:
            if t.transactionType == 'Expense':
                categorySummary[t.category] += t.amount
        print("\nExpenses by Category:")
        for category, total in categorySummary.items():
            print(f"{category}: ${total:.2f}")


def menu():
    tracker = BudgetTracker()
    while True:
        print("\n--- Budget Tracker ---")
        print("1. Add Monthly Income")
        print("2. Add Monthly Expenses")
        print("3. View Summary")
        print("4. View Expenses by Category")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            amount = input("Enter income amount: ")
            try:
                float(amount)
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            category = input("Enter income category (e.g., Salary, Pawning, Gambling, Side Work): ")
            tracker.addTransaction(Transaction(amount, category, 'Income'))

        elif choice == '2':
            amount = input("Enter expense amount: ")
            try:
                float(amount)
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            category = input("Enter expense category (e.g., Food, Clothes, Credit Card Payments, Debt): ")
            tracker.addTransaction(Transaction(amount, category, 'Expense'))

        elif choice == '3':
            tracker.viewSummary()

        elif choice == '4':
            tracker.viewByCategory()

        elif choice == '5':
            print("Exiting Budget Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
