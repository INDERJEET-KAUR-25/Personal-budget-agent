import json
import os
from datetime import datetime


class BudgetMemory:

    def __init__(self, budget_amount=15000):
        self.budget_amount = budget_amount
        self.data_file = os.path.join(
            os.path.dirname(__file__),
            "data",
            "expenses.json"
        )

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        self.data = self._load_data()
        self._initialize_current_month()

    # --------------------------------------------------
    # Load saved data
    # --------------------------------------------------

    def _load_data(self):

        if not os.path.exists(self.data_file):
            return {
                "months": {}
            }

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if "months" not in data:
                data["months"] = {}

            return data

        except (json.JSONDecodeError, OSError):
            return {
                "months": {}
            }

    # --------------------------------------------------
    # Save data
    # --------------------------------------------------

    def _save_data(self):

        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------------
    # Get current month
    # --------------------------------------------------

    def _get_current_month(self):

        return datetime.now().strftime("%Y-%m")

    # --------------------------------------------------
    # Initialize current month
    # --------------------------------------------------

    def _initialize_current_month(self):

        current_month = self._get_current_month()

        if current_month not in self.data["months"]:

            self.data["months"][current_month] = {
                "budget": self.budget_amount,
                "expenses": []
            }

            self._save_data()

        self.current_month = current_month

    # --------------------------------------------------
    # Current month's data
    # --------------------------------------------------

    @property
    def current_data(self):

        return self.data["months"][self.current_month]

    # --------------------------------------------------
    # Budget
    # --------------------------------------------------

    @property
    def budget(self):

        return self.current_data["budget"]

    def set_budget(self, amount):

        self.current_data["budget"] = amount
        self._save_data()

    # --------------------------------------------------
    # Add expense
    # --------------------------------------------------

    def add_expense(self, item, amount, category):

        self.current_data["expenses"].append({
            "item": item,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        self._save_data()

    # --------------------------------------------------
    # Get expenses
    # --------------------------------------------------

    def get_expenses(self):

        return self.current_data["expenses"]

    # --------------------------------------------------
    # Calculate total spending
    # --------------------------------------------------

    def get_total_spent(self):

        return sum(
            expense["amount"]
            for expense in self.current_data["expenses"]
        )

    # --------------------------------------------------
    # Calculate remaining budget
    # --------------------------------------------------

    def get_remaining_budget(self):

        return self.budget - self.get_total_spent()