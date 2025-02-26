import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
CHAT_ID = " 2351667124"  # Your group chat ID
TOPIC_ID = 6  # Replace with your actual topic ID

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json  # Expecting JSON data from the form submission
    full_name = data.get("name")
    date_from = data.get("date_from")
    date_till = data.get("date_till")
    reason = data.get("reason")
    eld = data.get("eld")

    if not full_name or not date_from or not date_till:
        return jsonify({"error": "Missing required fields"}), 400

    message = f"🚗 **TIME-OFF REQUEST** 🚗\n\n🔹 **Name:** {full_name}\n🔹 **Date Off:** {date_from} - {date_till}\n🔹 **Reason:** {reason}\n🔹 **Pause ELD?** {eld}"
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": TOPIC_ID,  # Send message inside the topic
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(telegram_url, json=payload)

    if response.status_code == 200:
        return jsonify({"message": "Request sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send message"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
