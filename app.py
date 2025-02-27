import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
NAME, DATE, REASON = range(3)

# Define the bot token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"

def start(update: Update, context: CallbackContext):
    """Start command handler"""
    update.message.reply_text("🚗 **OFF REQUEST FORM** 🚗\n\n🔹 Please enter your **Full Name**:")
    return NAME

def get_name(update: Update, context: CallbackContext):
    """Collect user's name"""
    context.user_data["name"] = update.message.text
    update.message.reply_text("🔹 Enter your **Date Off** (From):")
    return DATE

def get_date(update: Update, context: CallbackContext):
    """Collect user's date off information"""
    context.user_data["date"] = update.message.text
    update.message.reply_text("🔹 Enter the **Reason**:")
    return REASON

def get_reason(update: Update, context: CallbackContext):
    """Collect reason for time off"""
    context.user_data["reason"] = update.message.text
    name = context.user_data["name"]
    date = context.user_data["date"]
    reason = context.user_data["reason"]

    summary = (
        f"✅ **OFF REQUEST SUMMARY** ✅\n\n"
        f"🔹 **Name:** {name}\n"
        f"🔹 **Date Off:** {date}\n"
        f"🔹 **Reason:** {reason}\n"
    )
    
    # Send the message to the group thread (replace chat_id and thread_id with your actual values)
    chat_id = "-1002351667124"  # Group chat ID
    message_thread_id = 6  # Thread ID for the topic
    message = f"🚗 **TIME-OFF REQUEST** 🚗\n\n{name}\n**Date Off:** {date}\n**Reason:** {reason}"

    context.bot.send_message(chat_id=chat_id, text=message, message_thread_id=message_thread_id)

    update.message.reply_text("✅ Your request has been submitted!")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation"""
    update.message.reply_text("❌ **Form Canceled.**")
    return ConversationHandler.END

def main():
    """Start the bot"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation handler setup
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, get_date)],
            REASON: [MessageHandler(Filters.text & ~Filters.command, get_reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Add conversation handler to dispatcher
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
