import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

from memory import BudgetMemory
from tools import add_expense, get_summary


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Budget Memory
# ============================================================

memory = BudgetMemory()

# Initial budget for the assignment demo
memory.set_budget(15000)

def reset_budget():
    global memory

    memory = BudgetMemory()
    memory.set_budget(15000)


# ============================================================
# Define Agent Tools
# ============================================================

@tool
def add_expense_tool(item: str, amount: float, category: str):
    """
    Add an expense to the user's budget.

    Use this tool whenever the user reports a new expense.
    """

    return add_expense(
        memory,
        item,
        amount,
        category
    )


@tool
def get_summary_tool(category: str = ""):
    """
    Get the user's spending summary.

    Use this tool when the user asks about total spending,
    remaining budget, or spending in a particular category.
    """

    if category.strip() == "":
        category = None

    return get_summary(
        memory,
        category
    )


tools = [
    add_expense_tool,
    get_summary_tool
]


# ============================================================
# Foundry LLM
# ============================================================

llm = ChatOpenAI(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# Agent Node
# ============================================================

def agent_node(state: MessagesState):

    system_message = {
        "role": "system",
        "content": (
            "You are a personal budget assistant for tracking "
            "personal expenses and budgets.\n\n"

            "Rules:\n"
            "1. The currency is Indian Rupees (₹). Never use dollars.\n"

            "2. Always use the available tools when the user asks "
            "to add an expense or check spending.\n"

            "3. When categorizing expenses, use these categories:\n"
            "   - Food: groceries, restaurants, meals, snacks\n"
            "   - Travel: bus, train, metro, taxi, cab, fuel, transportation\n"
            "   - Shopping: clothes, electronics, accessories, online shopping\n"
            "   - Housing: rent and housing expenses\n"
            "   - Utilities: electricity, water, internet, phone\n"
            "   - Other: expenses that do not fit the above categories\n"

            "4. If the user does not explicitly provide a category, "
            "infer the most appropriate category.\n"

            "5. Always report monetary values using ₹.\n"

            "6. Do not invent spending information. Use the budget "
            "tools to obtain actual spending data.\n"

            "7. When reporting a budget summary, clearly state the "
            "total spent and remaining budget."
        )
    }

    messages = [system_message] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ============================================================
# Decide Whether to Continue to Tools
# ============================================================

def should_continue(state: MessagesState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# ============================================================
# Build LangGraph
# ============================================================

graph_builder = StateGraph(MessagesState)

graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "agent")

graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

graph_builder.add_edge("tools", "agent")


# ============================================================
# LangGraph Checkpoint Memory
# ============================================================

checkpointer = InMemorySaver()

agent = graph_builder.compile(
    checkpointer=checkpointer
)


# ============================================================
# Run Agent
# ============================================================

def run_agent(
    user_message: str,
    thread_id: str = "budget-user-1"
):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return result["messages"][-1].content


# ============================================================
# Run Agent + Trace
# ============================================================

def run_agent_with_trace(
    user_message: str,
    thread_id: str = "budget-user-1"
):
    """
    Run the agent and return the final response along with
    tool calls generated during the current interaction.
    """

    # Get the state before this interaction
    previous_state = agent.get_state(
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    previous_message_count = 0

    if previous_state and previous_state.values:
        previous_messages = previous_state.values.get(
            "messages",
            []
        )
        previous_message_count = len(previous_messages)

    # Run the current interaction
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    messages = result["messages"]

    # Only inspect messages generated during this interaction
    new_messages = messages[previous_message_count:]

    tool_calls = []

    for message in new_messages:

        if hasattr(message, "tool_calls") and message.tool_calls:

            for call in message.tool_calls:

                tool_calls.append({
                    "tool": call["name"],
                    "arguments": call["args"]
                })

    return {
        "response": messages[-1].content,
        "tool_calls": tool_calls
    }

# ============================================================
# Interactive Terminal Demo
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PERSONAL BUDGET AGENT")
    print("=" * 60)

    print("\nBudget: ₹15,000")
    print("Type 'exit' to quit.")

    thread_id = "budget-user-1"

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":

            print("\nGoodbye!")
            break

        response = run_agent(
            user_input,
            thread_id
        )

        print("\nAgent:", response)