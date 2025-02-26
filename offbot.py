import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"

# Chat IDs for different topics
TIME_OFF_CHAT_ID = "7122508724"
ELD_CHAT_ID = "7122508724"

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json  # Expecting JSON data from the form submission
    full_name = data.get("name")
    date_from = data.get("date_from")
    date_till = data.get("date_till")
    reason = data.get("reason")
    pause_eld = data.get("eld")

    if not full_name or not date_from or not date_till:
        return jsonify({"error": "Missing required fields"}), 400

    # Message for the Time-Off topic
    time_off_message = f"🚗 **TIME-OFF REQUEST** 🚗\n🔹 **Driver:** {full_name}\n🔹 **Time Off:** {date_from} - {date_till}\n🔹 **Reason:** {reason}"
    
    # Message for the ELD topic (if pause is requested)
    if pause_eld.lower() == "yes":
        eld_message = f"⏸ **PAUSE ELD REQUEST** ⏸\n🔹 **Driver:** {full_name}\n🔹 **Time Off:** {date_from} - {date_till}\n🔹 **Please pause ELD for this driver.**"

    # Send Time-Off Request
    send_telegram_message(TIME_OFF_CHAT_ID, time_off_message)

    # Send ELD Pause Request if necessary
    if pause_eld.lower() == "yes":
        send_telegram_message(ELD_CHAT_ID, eld_message)

    return jsonify({"message": "Requests sent successfully!"}), 200

def send_telegram_message(chat_id, message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(telegram_url, json=payload)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
