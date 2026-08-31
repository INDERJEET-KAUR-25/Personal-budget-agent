const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");


function addMessage(message, type) {

    const container = document.createElement("div");

    container.className = "message " + type;


    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        type === "user" ? "You" : "AI";


    const bubble = document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = message;


    container.appendChild(avatar);
    container.appendChild(bubble);

    chatBox.appendChild(container);


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    addMessage(message, "user");


    input.value = "";

    sendButton.disabled = true;

    sendButton.textContent = "...";


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });


        const data =
            await response.json();


        addMessage(
            data.response,
            "bot"
        );


        // Update dashboard
        // directly from BudgetMemory

        await loadSummary();


    } catch (error) {

        addMessage(
            "Sorry, something went wrong while connecting to the budget agent.",
            "bot"
        );

        console.error(error);

    }


    sendButton.disabled = false;

    sendButton.textContent = "Send";
}


async function loadSummary() {

    try {

        const response =
            await fetch("/summary");


        const data =
            await response.json();


        /*
         * Update summary cards
         */

        document.getElementById(
            "total-spent"
        ).textContent =
            "₹" + data.total_spent.toLocaleString("en-IN");


        document.getElementById(
            "remaining-budget"
        ).textContent =
            "₹" + data.remaining_budget.toLocaleString("en-IN");


        /*
         * Update spending percentage
         */

        const percentage =
            data.budget > 0
                ? Math.round(
                    (data.total_spent /
                    data.budget) * 100
                )
                : 0;


        document.getElementById(
            "percentage"
        ).textContent =
            percentage + "%";


        /*
         * Update donut chart
         */

        const degrees =
            Math.min(percentage, 100) * 3.6;


        document.querySelector(
            ".donut"
        ).style.background =
            `conic-gradient(
                #111827 ${degrees}deg,
                #e5e7eb ${degrees}deg
            )`;


        /*
         * Update category totals
         */

        let food = 0;
        let travel = 0;
        let other = 0;


        data.expenses.forEach(expense => {

            const category =
                expense.category.toLowerCase();


            if (category === "food") {

                food += expense.amount;

            } else if (category === "travel") {

                travel += expense.amount;

            } else {

                other += expense.amount;

            }

        });


        document.getElementById(
            "food-amount"
        ).textContent =
            "₹" + food.toLocaleString("en-IN");


        document.getElementById(
            "travel-amount"
        ).textContent =
            "₹" + travel.toLocaleString("en-IN");


        document.getElementById(
            "other-amount"
        ).textContent =
            "₹" + other.toLocaleString("en-IN");


        /*
         * Update recent expenses
         */

        const expenseList =
            document.getElementById(
                "expense-list"
            );


        if (data.expenses.length === 0) {

            expenseList.innerHTML =
                '<div class="empty-state">' +
                'No expenses added yet.' +
                '</div>';

            return;
        }


        expenseList.innerHTML = "";


        data.expenses
            .slice()
            .reverse()
            .slice(0, 5)
            .forEach(expense => {

                const row =
                    document.createElement("div");

                row.className =
                    "table-row";


                row.innerHTML = `
                    <span>${expense.item}</span>

                    <span>${expense.category}</span>

                    <span>
                        ₹${expense.amount.toLocaleString("en-IN")}
                    </span>
                `;


                expenseList.appendChild(row);

            });


    } catch (error) {

        console.error(
            "Could not load summary:",
            error
        );

    }
}


/*
 * Send message when button is clicked.
 */

sendButton.addEventListener(
    "click",
    sendMessage
);


/*
 * Send message when Enter is pressed.
 */

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


/*
 * Load dashboard when page opens.
 */

loadSummary();