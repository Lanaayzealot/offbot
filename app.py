from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging

# Telegram Bot Token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"

# Thread IDs
SOURCE_THREAD_ID = 6  # Fetch requests from this thread
TARGET_THREAD_ID = 2  # Send ELD turn-off messages to this thread
CHAT_ID = "-1002351667124"  # Replace with your group chat ID

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Conversation states
NAME, DATE, REASON = range(3)

def start(update: Update, context: CallbackContext):
    """Initiate the off request conversation."""
    update.message.reply_text("🚗 OFF REQUEST FORM 🚗\n\n🔹 Please enter your Full Name:")
    return NAME

def get_name(update: Update, context: CallbackContext):
    """Store the user's name and ask for the date off."""
    context.user_data["name"] = update.message.text
    update.message.reply_text("🔹 Enter your Date Off (MM/DD/YYYY):")
    return DATE

def get_date(update: Update, context: CallbackContext):
    """Store the date off and ask for the reason."""
    context.user_data["date"] = update.message.text
    update.message.reply_text("🔹 Enter the Reason:")
    return REASON

def get_reason(update: Update, context: CallbackContext):
    """Store the reason and send the request."""
    context.user_data["reason"] = update.message.text
    name = context.user_data["name"]
    date = context.user_data["date"]
    reason = context.user_data["reason"]

    # Time-off request summary
    summary = (
        f"✅ OFF REQUEST SUMMARY ✅\n\n"
        f"🔹 Name: {name}\n"
        f"🔹 Date Off: {date}\n"
        f"🔹 Reason: {reason}\n"
    )
    
    # Send confirmation to user
    update.message.reply_text(summary)

    # Forward ELD Turn-Off Notification to Topic ID 2
    eld_message = (
        f"⚠️ **TURN OFF ELD** ⚠️\n\n"
        f"🔹 Name: {name}\n"
        f"🔹 Date Off: {date}\n"
        f"🔹 Reason: {reason}\n"
        f"🔹 Action Required: Turn off ELD for this user."
    )

    context.bot.send_message(chat_id=CHAT_ID, message_thread_id=TARGET_THREAD_ID, text=eld_message)

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    """Handle cancellation of the form."""
    update.message.reply_text("❌ Form Canceled.")
    return ConversationHandler.END

def handle_topic_messages(update: Update, context: CallbackContext):
    """Fetch messages from thread ID 6 and process them."""
    if update.message.message_thread_id == SOURCE_THREAD_ID:
        text = update.message.text
        if "Date Off:" in text and "Name:" in text:
            # Extract name, date, and reason (Basic parsing)
            lines = text.split("\n")
            name = lines[1].split(": ")[1] if len(lines) > 1 else "Unknown"
            date = lines[2].split(": ")[1] if len(lines) > 2 else "Unknown"
            reason = lines[3].split(": ")[1] if len(lines) > 3 else "Unknown"

            # Send ELD Turn-Off Notification
            eld_message = (
                f"⚠️ **TURN OFF ELD** ⚠️\n\n"
                f"🔹 Name: {name}\n"
                f"🔹 Date Off: {date}\n"
                f"🔹 Reason: {reason}\n"
                f"🔹 Action Required: Turn off ELD for this user."
            )

            context.bot.send_message(chat_id=CHAT_ID, message_thread_id=TARGET_THREAD_ID, text=eld_message)

def main():
    """Main function to start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation handler for user input
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, get_date)],
            REASON: [MessageHandler(Filters.text & ~Filters.command, get_reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)

    # Listen for messages in thread ID 6 and process them
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic_messages))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
