import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
CHAT_ID = " 2351667124"  # Your group chat ID
TOPIC_ID = 6  # Replace with your actual topic ID

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_GROUP_CHAT_ID"

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json  # Expecting JSON data from the form submission
    full_name = data.get("name")
    date_from = data.get("date_from")
    date_till = data.get("date_till")

    if not full_name or not date_from or not date_till:
        return jsonify({"error": "Missing required fields"}), 400

    message = f"🚛 **ELD PAUSE REQUEST** 🚛\n🔹 **Driver:** {full_name}\n🔹 **Time Off:** {date_from} - {date_till}\n🔹 **Please pause ELD for this driver.**"
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(telegram_url, json=payload)

    if response.status_code == 200:
        return jsonify({"message": "Request sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send message"}), 500


# Webhook to handle incoming Telegram updates
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Get the incoming JSON data from Telegram
    print(data)  # For debugging purposes, print the incoming data
    
    # Here, you can process the incoming message and take action, like sending a reply to the user
    # Example: Send a simple confirmation message back (if needed):
    # reply_message = "Got your message!"
    # telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # payload = {"chat_id": data['message']['chat']['id'], "text": reply_message}
    # response = requests.post(telegram_url, json=payload)

    return jsonify({"status": "ok"})  # Respond to Telegram that the request was received successfully


if __name__ == "__main__":
    app.run(port=5000, debug=True)
