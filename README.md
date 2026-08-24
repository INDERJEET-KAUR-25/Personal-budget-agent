# Personal Budget Agent

An Agentic AI-based personal budget assistant built using **Microsoft Foundry, GPT-4.1-mini, LangChain, and LangGraph**.

The agent allows users to interact with their personal budget using natural language. It can identify expenses, automatically categorize them, store them in memory, calculate total spending, determine the remaining budget, and answer category-specific spending queries.

---

## 1. Project Overview

Managing personal expenses manually can be inconvenient, especially when users need to repeatedly calculate their total spending and remaining budget.

The **Personal Budget Agent** addresses this problem by providing a natural-language interface for basic personal budget management.

Instead of requiring users to enter structured commands, they can simply say:

> "I spent ₹1200 on groceries."

The agent interprets the request, selects the appropriate tool, extracts the required information, updates the budget memory, and generates a natural-language response.

For example:

```text
User:
I spent ₹1200 on groceries.

Agent:
I have added your expense of ₹1200 for groceries under the Food category.

The agent can also answer:

User:
How much have I spent in total and how much budget do I have left?

Agent:
You have spent a total of ₹1700 so far.
Your remaining budget is ₹13,300.


2. Objectives

The main objectives of this project are:

Build a simple Agentic AI application.
Use Microsoft Foundry and GPT-4.1-mini as the language model.
Use LangGraph to implement a stateful agent workflow.
Allow the LLM to select tools based on user requests.
Maintain budget and expense information using in-memory state.
Automatically categorize expenses.
Calculate total spending and remaining budget.
Demonstrate tool-calling traces in a Jupyter notebook.
Evaluate the agent using multiple test scenarios.
3. Key Features
Natural-Language Expense Entry

Users can enter expenses using normal language.

Example:

I spent ₹1200 on groceries.

The agent extracts:

Item       → groceries
Amount     → ₹1200
Category   → Food
Automatic Expense Categorization

The agent categorizes expenses using predefined categories:

Category	Examples
Food	groceries, restaurants, meals, snacks
Travel	bus, train, metro, taxi, cab, fuel
Housing	rent and housing expenses
Utilities	electricity, water, internet, phone
Other	expenses that do not fit the above categories
Budget Tracking

The application maintains:

Total budget
Individual expenses
Total spending
Remaining budget

Example:

Budget       = ₹15,000
Groceries    = ₹1,200
Bus          = ₹500
--------------------
Total spent  = ₹1,700
Remaining    = ₹13,300
Category-Based Analysis

Users can ask:

How much did I spend on food?

The agent can retrieve spending for a particular category.

Agentic Tool Calling

The LLM decides which tool is required for a particular user request.

The project currently provides two tools:

add_expense_tool
get_summary_tool
Stateful Agent Workflow

LangGraph is used to manage the agent workflow and conversation state.

The workflow follows:

User Request
     ↓
GPT-4.1-mini
     ↓
LangGraph Agent
     ↓
Tool Selection
     ↓
Tool Execution
     ↓
BudgetMemory
     ↓
Tool Result
     ↓
Agent Response
4. System Architecture

The overall architecture consists of four major layers.

4.1 User Layer

The user interacts with the system using natural-language requests.

Example:

I spent ₹500 on the bus.
4.2 LLM Layer

GPT-4.1-mini, deployed through Microsoft Foundry, interprets the user's request and determines whether a tool is required.

4.3 Agent and Tool Layer

LangGraph manages the agent workflow.

The available tools are:

add_expense_tool

Used when the user provides a new expense.

Parameters:

item
amount
category
get_summary_tool

Used when the user asks for spending or budget information.

Optional parameter:

category
4.4 Memory Layer

BudgetMemory stores the current budget and expenses in Python memory.

It maintains:

Budget
Expenses
Total Spending
Remaining Budget
5. Agent Workflow

The LangGraph workflow is implemented using:

StateGraph
MessagesState
ToolNode
InMemorySaver

The workflow is:

             ┌───────────────┐
             │   User Input  │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ GPT-4.1-mini  │
             │    Agent      │
             └───────┬───────┘
                     │
              Tool required?
                /          \
              Yes           No
               │             │
               ▼             ▼
        ┌────────────┐   ┌────────┐
        │  ToolNode  │   │  END   │
        └─────┬──────┘   └────────┘
              │
              ▼
       ┌──────────────┐
       │ BudgetMemory │
       └──────┬───────┘
              │
              ▼
        Tool Result
              │
              ▼
        ┌────────────┐
        │   Agent    │
        └─────┬──────┘
              │
              ▼
        Final Response
6. Technologies Used
Technology	Purpose
Python	Core programming language
Microsoft Foundry	AI model platform
GPT-4.1-mini	Language model
LangChain	LLM and tool integration
LangGraph	Agent workflow and state management
python-dotenv	Environment variable management
Jupyter Notebook	Demonstration and evaluation
7. Project Structure
Budget-Agent/
│
├── agent.py
├── app.py
├── budget_agent_demo.ipynb
├── memory.py
├── prompts.py
├── tools.py
├── test_llm.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│
└── screenshots/
File Description
File	Description
agent.py	Main LangGraph agent implementation
app.py	Basic budget application/demo
memory.py	Budget and expense memory implementation
tools.py	Expense and summary tool functions
prompts.py	Prompt-related file
test_llm.py	LLM connection test
budget_agent_demo.ipynb	Complete notebook demonstration and evaluation
requirements.txt	Python dependencies
screenshots/	Project screenshots
data/	Project data directory
8. Installation
Step 1: Clone or download the project
git clone <your-repository-url>
cd Budget-Agent
Step 2: Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
Step 3: Install dependencies
pip install -r requirements.txt

If required, the main packages include:

pip install langchain
pip install langchain-openai
pip install langgraph
pip install python-dotenv
9. Microsoft Foundry Setup

This project uses GPT-4.1-mini deployed through Microsoft Foundry.

The model used in the project is:

Model: GPT-4.1-mini
Version: 2025-04-14
Deployment Type: Global Standard

The deployment was created in Microsoft Foundry and successfully tested through the application.

Note: Model availability and supported deployment regions can vary depending on the Azure subscription and region.

10. Environment Variables

Create a .env file in the project root.

Example structure:

OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
OPENAI_BASE_URL=your_base_url

Do not commit real API keys or credentials to GitHub.

The .env file should remain private.

11. Running the Application

Activate the virtual environment:

venv\Scripts\activate

Then run:

python agent.py

The application starts with:

============================================================
PERSONAL BUDGET AGENT
============================================================

Budget: ₹15,000
Type 'exit' to quit.
12. Example Interaction
Adding an Expense
You: I spent ₹1200 on groceries.

Agent:
I have added your expense of ₹1200 for groceries under the Food category.
Adding Another Expense
You: I spent ₹500 on the bus.

Agent:
I have added your expense of ₹500 for the bus under the Travel category.
Checking Total Spending
You:
How much have I spent in total and how much budget do I have left?

Agent:
You have spent a total of ₹1700 so far.
Your remaining budget is ₹13,300.
13. Agent Tools
Tool 1: add_expense_tool

Purpose:

Add a new expense to the budget.

Example tool call:

{
    "tool": "add_expense_tool",
    "arguments": {
        "item": "groceries",
        "amount": 1200,
        "category": "Food"
    }
}
Tool 2: get_summary_tool

Purpose:

Retrieve overall or category-specific spending information.

Example:

{
    "tool": "get_summary_tool",
    "arguments": {}
}

Category-specific example:

{
    "tool": "get_summary_tool",
    "arguments": {
        "category": "Food"
    }
}
14. Memory

The project uses a custom BudgetMemory class.

It stores:

budget
expenses

Each expense is represented using:

{
    "item": "...",
    "amount": ...,
    "category": "..."
}

The memory provides functions for:

set_budget()
add_expense()
get_expenses()
get_total_spent()
get_remaining_budget()

The current implementation uses in-memory Python objects rather than a persistent database.

15. Notebook Demonstration

The project includes:

budget_agent_demo.ipynb

The notebook demonstrates:

System architecture
Expense addition
Multi-turn interaction
Category-based spending
Remaining budget calculation
Agentic tool-calling trace
Evaluation results
Limitations
Final workflow
Final clean demonstration

The final demonstration uses a fresh budget state.

Final Demonstration Results
Initial Budget: ₹15,000

Groceries: ₹1,200
Bus: ₹500

Total Spending: ₹1,700
Remaining Budget: ₹13,300
16. Evaluation

The agent was evaluated using multiple natural-language scenarios.

Test Case	Expected Result	Status
Add ₹1,200 groceries	Food category	Pass
Add ₹500 bus	Travel category	Pass
Check total spending	₹1,700	Pass
Check Food spending	₹1,200	Pass
Check remaining budget	₹13,300	Pass
Expense tool selection	add_expense_tool	Pass
Summary tool selection	get_summary_tool	Pass

The clean tool-calling trace confirms that the agent selects the appropriate tool for the user's request.

17. Agentic AI Characteristics Demonstrated

The project demonstrates several characteristics of an Agentic AI system:

Perception / Understanding

The LLM interprets natural-language user requests.

Decision Making

The LLM determines whether the request requires an expense tool or summary tool.

Tool Use

The agent invokes external Python functions through LangGraph tool calling.

State

Budget and expense information are maintained in memory.

Feedback

Tool results are returned to the agent, which then generates the final natural-language response.

18. Limitations

The current implementation has several limitations:

Budget information is stored in memory and is not persisted to a database.
The current budget is initialized to a fixed value of ₹15,000.
InMemorySaver is used for demonstration of conversation state.
The application does not currently implement user authentication.
There is no graphical user interface.
Expense categories are inferred by the LLM and may occasionally require clarification.
The current implementation is intended as an educational Agentic AI demonstration.
19. Future Scope

The system can be extended with:

Persistent database storage.
User authentication and multiple user accounts.
Web or mobile interface.
Monthly and yearly budget management.
Spending visualization dashboards.
Budget alerts and notifications.
Recurring expense detection.
Personalized spending recommendations.
Expense import from bank statements.
More advanced financial analytics.

20. Conclusion

The Personal Budget Agent demonstrates a practical implementation of an Agentic AI workflow using Microsoft Foundry, GPT-4.1-mini, LangChain, and LangGraph.

The system can interpret natural-language budget requests, select appropriate tools, update and retrieve budget information, maintain state, and provide meaningful responses to users.

The core workflow is:

User Request
      ↓
LLM Understanding
      ↓
Tool Selection
      ↓
Tool Execution
      ↓
Memory / State
      ↓
Tool Result
      ↓
Final Agent Response

The project provides a simple foundation for building more advanced AI-powered personal finance assistants.


