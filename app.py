from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re

# Define the Telegram bot token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
GROUP_CHAT_ID = "-1002351667124"  # Replace with your Telegram group chat ID
THREAD_ID_6 = 6  # Replace with your thread ID 6
THREAD_ID_2 = 2  # Replace with your thread ID 2

# Define the label you want to apply
LABEL = "[Label]"

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! I'm here to help you apply labels to messages in the group.")

# Function to capture the driver's full name from a message
def extract_full_name(message_text: str) -> str:
    # Assuming the full name is structured as "First Last" and it's the first part of the message.
    # Modify the regex as per your requirement
    match = re.match(r"([A-Za-z]+ [A-Za-z]+)", message_text)
    if match:
        return match.group(1)
    return None

# Function to send a message to Thread ID 2 asking to pause the ELD for the driver's full name
async def send_pause_request(driver_name: str, context: CallbackContext):
    # Format the message to be sent to thread ID 2
    pause_request_message = f"Please pause the ELD for driver: {driver_name}"
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=pause_request_message,
        reply_to_message_id=None,  # No reply to message in thread
        message_thread_id=THREAD_ID_2  # Send message to thread 2
    )

# Function to label the message and request pause for ELD if needed
async def label_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    if message_text and update.message.chat.id == int(GROUP_CHAT_ID):
        # Add a label to the message
        label_text = f"{LABEL} {message_text}"

        # Send a new message with the label in the thread
        await update.message.reply_text(
            label_text,
            reply_to_message_id=update.message.message_id,
            message_thread_id=THREAD_ID_6  # Send message to thread 6
        )

        # Extract the driver's full name (assuming it's in the message text)
        driver_name = extract_full_name(message_text)
        if driver_name:
            # If a full name is found, send a pause request to thread 2
            await send_pause_request(driver_name, context)

# Main function to start the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, label_message))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
