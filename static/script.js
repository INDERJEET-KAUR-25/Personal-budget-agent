const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");


function formatRupees(amount) {

    return "₹" + Number(amount).toLocaleString("en-IN");

}


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


function quickPrompt(message) {

    input.value = message;

    sendMessage();

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


        await loadSummary();


    } catch (error) {

        console.error(error);


        addMessage(
            "Sorry, I couldn't connect to the budget agent.",
            "bot"
        );

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


        const budget =
            Number(data.budget);


        const spent =
            Number(data.total_spent);


        const remaining =
            Number(data.remaining_budget);


        const percentage =
            budget > 0
                ? Math.round(
                    (spent / budget) * 100
                )
                : 0;


        /*
         * Summary cards
         */

        document.getElementById(
            "total-budget"
        ).textContent =
            formatRupees(budget);


        document.getElementById(
            "total-spent"
        ).textContent =
            formatRupees(spent);


        document.getElementById(
            "remaining-budget"
        ).textContent =
            formatRupees(remaining);


        document.getElementById(
            "percentage"
        ).textContent =
            percentage + "%";


        /*
         * Budget overview
         */

        document.getElementById(
            "percentage-center"
        ).textContent =
            percentage + "%";


        document.getElementById(
            "spent-overview"
        ).textContent =
            formatRupees(spent);


        document.getElementById(
            "remaining-overview"
        ).textContent =
            formatRupees(remaining);


        /*
         * Progress bar
         */

        document.getElementById(
            "progress-fill"
        ).style.width =
            Math.min(percentage, 100) + "%";


        /*
         * Donut chart
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
         * Category totals
         */

        const categories = {

            Food: 0,

            Travel: 0,

            Housing: 0,

            Utilities: 0,

            Other: 0

        };


        data.expenses.forEach(expense => {

            const category =
                expense.category;


            if (
                Object.prototype.hasOwnProperty.call(
                    categories,
                    category
                )
            ) {

                categories[category] +=
                    Number(expense.amount);

            } else {

                categories.Other +=
                    Number(expense.amount);

            }

        });


        document.getElementById(
            "food-amount"
        ).textContent =
            formatRupees(categories.Food);


        document.getElementById(
            "travel-amount"
        ).textContent =
            formatRupees(categories.Travel);


        document.getElementById(
            "housing-amount"
        ).textContent =
            formatRupees(categories.Housing);


        document.getElementById(
            "utilities-amount"
        ).textContent =
            formatRupees(categories.Utilities);


        document.getElementById(
            "other-amount"
        ).textContent =
            formatRupees(categories.Other);


        /*
         * Recent expenses
         */

        const expenseList =
            document.getElementById(
                "expense-list"
            );


        if (
            !data.expenses ||
            data.expenses.length === 0
        ) {

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
            .slice(0, 8)
            .forEach(expense => {

                const row =
                    document.createElement("div");


                row.className =
                    "table-row";


                row.innerHTML = `

                    <span>
                        ${escapeHtml(expense.item)}
                    </span>

                    <span>
                        ${escapeHtml(expense.category)}
                    </span>

                    <span>
                        ${formatRupees(expense.amount)}
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
 * Prevent HTML injection
 */

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;

}


/*
 * Button click
 */

sendButton.addEventListener(
    "click",
    sendMessage
);


/*
 * Enter key
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
 * Initial dashboard load
 */

loadSummary();