from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import asyncio

app = Flask(__name__)

# 🔹 Replace these with your actual values
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
GROUP_CHAT_ID = "-1002351667124"  # Telegram group chat ID
THREAD_ID_59 = 59  # Source thread (where driver names come from)
THREAD_ID_61 = 61  # Destination thread (where message is sent)

# Store the latest driver name
latest_driver_name = None

async def store_driver_name(update: Update, context: CallbackContext):
    """Capture messages from thread 59 and store the driver's name."""
    global latest_driver_name
    if update.message and update.message.message_thread_id == THREAD_ID_59:
        latest_driver_name = update.message.text.strip()  # Store the name

async def send_eld_pause_request(context: CallbackContext):
    """Send message to thread ID 61."""
    if latest_driver_name:
        message_text = f"🚛 Please pause the ELD for {latest_driver_name}."
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=message_text,
            message_thread_id=THREAD_ID_61  # Ensure topics are enabled in the group
        )

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook requests from Telegram."""
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    asyncio.create_task(application.process_update(update))  # Process update asynchronously
    return "OK", 200

async def main():
    """Start the Telegram bot."""
    global application
    application = Application.builder().token(TOKEN).build()

    # Register message handler for thread 59
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store_driver_name))

    # Start bot polling
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Run Telegram bot
    app.run(host='0.0.0.0', port=5000)  # Run Flask webhook
