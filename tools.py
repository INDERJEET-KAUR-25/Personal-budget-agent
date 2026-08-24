from memory import BudgetMemory


def add_expense(memory, item, amount, category):
    """
    Add an expense to the user's budget memory.
    """

    memory.add_expense(item, amount, category)

    return {
        "success": True,
        "message": f"Expense added: {item} - ₹{amount}",
        "item": item,
        "amount": amount,
        "category": category
    }


def get_summary(memory, category=None):
    """
    Get spending summary for a category or overall spending.
    """

    expenses = memory.get_expenses()

    if category:
        filtered_expenses = [
            expense
            for expense in expenses
            if expense["category"].lower() == category.lower()
        ]
    else:
        filtered_expenses = expenses

    total = sum(
        expense["amount"]
        for expense in filtered_expenses
    )

    return {
        "category": category if category else "All",
        "total_spent": total,
        "budget": memory.budget,
        "remaining_budget": memory.get_remaining_budget(),
        "expenses": filtered_expenses
    }