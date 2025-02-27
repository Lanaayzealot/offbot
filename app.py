from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

app = Flask(__name__)

# Define the Telegram bot token
TOKEN = "7001677306:AAEJAEzCghnWuhPrOwebvivD789BXn-6wm4"
GROUP_CHAT_ID = "-1002351667124"  # Replace with your Telegram group chat ID
THREAD_ID_6 = 6  # The thread ID from which you want to grab the driver's full name
THREAD_ID_2 = 2  # The thread ID to send the message to
LABEL = "[Label]"

# Function to get the driver's full name from the thread
async def get_driver_full_name(update: Update, context: CallbackContext):
    # Retrieve the thread ID 6 messages
    messages = await update.message.chat.get_messages(thread_id=THREAD_ID_6)
    
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
        # Compose the message to send to thread ID 2
        message_text = f"Please pause the ELD for {driver_full_name}."
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=
