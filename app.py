from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Define the Telegram bot token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
GROUP_CHAT_ID = "-100XXXXXXXXXXX"  # Replace with your Telegram group chat ID
THREAD_ID = 123  # Replace with your topic's thread ID (optional)

# Define the label you want to apply
LABEL = "[Label]"

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! I'm here to help you apply labels to messages in the group.")

# Function to reply with a label to a message
async def label_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    if message_text and update.message.chat.id == int(GROUP_CHAT_ID):
        # Add a label to the message
        label_text = f"{LABEL} {message_text}"

        # Send a new message with the label in the topic (thread)
        await update.message.reply_text(
            label_text,
            reply_to_message_id=update.message.message_id,
            message_thread_id=THREAD_ID  # If you're using a thread, provide the thread ID here
        )

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
