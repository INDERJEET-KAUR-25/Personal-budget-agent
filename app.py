from memory import BudgetMemory
from tools import add_expense, get_summary


memory = BudgetMemory()

# Set budget
memory.set_budget(15000)

# Add expenses
result1 = add_expense(
    memory,
    "Groceries",
    1200,
    "Food"
)

result2 = add_expense(
    memory,
    "Bus",
    500,
    "Travel"
)

print(result1)
print(result2)

# Get summary
summary = get_summary(memory)

print("\nSUMMARY")
print("Total spent:", summary["total_spent"])
print("Remaining budget:", summary["remaining_budget"])