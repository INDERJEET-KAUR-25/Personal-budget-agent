from flask import Flask, render_template, request, jsonify

from agent import run_agent, memory

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "response": "Please enter a message."
        })

    try:

        response = run_agent(
            user_message,
            thread_id="web-user-1"
        )

        return jsonify({
            "response": response
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        }), 500


@app.route("/summary")
def summary():

    total_spent = memory.get_total_spent()
    remaining = memory.get_remaining_budget()

    return jsonify({
        "budget": memory.budget,
        "total_spent": total_spent,
        "remaining_budget": remaining,
        "expenses": memory.get_expenses()
    })


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )