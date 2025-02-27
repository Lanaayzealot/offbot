import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
)

TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
CHAT_ID = "-1002351667124"  # Your group chat ID
FETCH_THREAD_ID = 6  # Topic where users request time-off
SEND_THREAD_ID = 2  # Topic to send ELD turn-off request

# Conversation states
NAME, DATE_FROM, DATE_TILL, REASON = range(4)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    """Start the time-off request process."""
    await update.message.reply_text("🚗 OFF REQUEST FORM 🚗\n\n🔹 Please enter your Full Name:")
    return NAME


async def get_name(update: Update, context: CallbackContext):
    """Store the user's name and ask for the time-off start date."""
    context.user_data["name"] = update.message.text
    await update.message.reply_text("🔹 Enter your Date Off (From) (MM/DD/YYYY):")
    return DATE_FROM


async def get_date_from(update: Update, context: CallbackContext):
    """Store the start date and ask for the end date."""
    context.user_data["date_from"] = update.message.text
    await update.message.reply_text("🔹 Enter your Date Off (Till) (MM/DD/YYYY):")
    return DATE_TILL


async def get_date_till(update: Update, context: CallbackContext):
    """Store the end date and ask for the reason."""
    context.user_data["date_till"] = update.message.text
    await update.message.reply_text("🔹 Enter the Reason for your time-off:")
    return REASON


async def get_reason(update: Update, context: CallbackContext):
    """Store the reason, check if more than a week, and send the request."""
    context.user_data["reason"] = update.message.text
    name = context.user_data["name"]
    date_from = context.user_data["date_from"]
    date_till = context.user_data["date_till"]
    reason = context.user_data["reason"]

    # Prepare the message
    message = (
        f"🚗 TIME-OFF REQUEST 🚗\n\n"
        f"🔹 Name: {name}\n"
        f"🔹 Date Off: From {date_from} Till {date_till}\n"
        f"🔹 Reason: {reason}"
    )

    # Send message to the request topic (Thread ID 6)
    await send_telegram_message(FETCH_THREAD_ID, message)

    # Check if requested period is more than 7 days
    from datetime import datetime

    try:
        date_format = "%m/%d/%Y"
        start_date = datetime.strptime(date_from, date_format)
        end_date = datetime.strptime(date_till, date_format)
        delta = (end_date - start_date).days

        if delta > 7:
            eld_message = (
                f"🔴 ELD PAUSE REQUEST 🔴\n\n"
                f"🔹 Name: {name}\n"
                f"🔹 Date Off: {date_from} - {date_till}\n"
                f"🔹 Reason: {reason}\n"
                f"⚠️ Requested period exceeds 7 days. Pause ELD needed!"
            )

            # Send message to the ELD topic (Thread ID 2)
            await send_telegram_message(SEND_THREAD_ID, eld_message)
    except Exception as e:
        logger.error(f"Date parsing error: {e}")

    await update.message.reply_text("✅ Your request has been submitted.")
    return ConversationHandler.END


async def send_telegram_message(thread_id, message):
    """Send a message to a specific Telegram topic thread."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "message_thread_id": thread_id,
        "text": message,
    }
    
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            if not result.get("ok"):
                logger.error(f"Failed to send message: {result}")


async def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    await update.message.reply_text("❌ Form Canceled.")
    return ConversationHandler.END


def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date_from)],
            DATE_TILL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date_till)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
