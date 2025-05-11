# expense_manager.py
import csv
import os
from datetime import datetime

class Expense:
    def __init__(self, amount, category, description):
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "Date": self.date,
            "Amount": self.amount,
            "Category": self.category,
            "Description": self.description
        }

class ExpenseTracker:
    def __init__(self, file_path="data/expenses.csv"):
        self.file_path = file_path
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(file_path):
            with open(file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
                writer.writeheader()

    def add_expense(self, expense: Expense):
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
            writer.writerow(expense.to_dict())

    def get_expenses(self):
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def delete_expense(self, description: str):
        expenses = self.get_expenses()
        updated_expenses = [expense for expense in expenses if expense["Description"] != description]
        
        with open(self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
            writer.writeheader()
            writer.writerows(updated_expenses)
