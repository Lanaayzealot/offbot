from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

app = Flask(__name__)

# Define the Telegram bot token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
GROUP_CHAT_ID = "-1002351667124"  # Replace with your Telegram group chat ID
THREAD_ID_59 = 59  # The thread ID from which you want to grab the driver's full name
THREAD_ID_61 = 61  # The thread ID to send the message to
LABEL = "[Label]"

# Function to get the driver's full name from the thread
async def get_driver_full_name(update: Update, context: CallbackContext):
    # Retrieve the thread ID 6 messages
    messages = await update.message.chat.get_messages(thread_id=THREAD_ID_59)
    
    # Loop through messages in the thread to find the full name
    for message in messages:
        if message.text:
            # Assuming the full name is in the message text
            driver_full_name = message.text.strip()  # Modify this logic based on how full name is provided
            return driver_full_name

    return None

# Function to send message asking to pause ELD
async def ask_to_pause_eld(driver_full_name, context: CallbackContext):
    if driver_full_name:
        # Compose the message to send to thread ID 61
        message_text = f"Please pause the ELD for {driver_full_name}."
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=message_text,
            reply_to_message_id=None,
            message_thread_id=THREAD_ID_61
        )

# Flask route to handle incoming webhook requests
@app.route('/webhook', methods=['POST'])
def webhook():
    # Process the incoming update
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    application.process_update(update)

    return "OK", 200

# Main function to start the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Register handlers for different commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, label_message))

    # Start the bot
    await application.run_polling()

# Flask entry point to start the server
if __name__ == '__main__':
    # Ensure that the bot is running alongside the Flask app
    import asyncio
    asyncio.run(main())
    app.run(host='0.0.0.0', port=5000)
