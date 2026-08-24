class BudgetMemory:
    def __init__(self):
        self.budget = 0
        self.expenses = []

    def set_budget(self, amount):
        self.budget = amount

    def add_expense(self, item, amount, category):
        self.expenses.append({
            "item": item,
            "amount": amount,
            "category": category
        })

    def get_expenses(self):
        return self.expenses

    def get_total_spent(self):
        return sum(expense["amount"] for expense in self.expenses)

    def get_remaining_budget(self):
        return self.budget - self.get_total_spent()