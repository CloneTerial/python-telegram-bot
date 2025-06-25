from telegram import Update
from telegram.ext import ContextTypes
from Command_Handler import plugin

@plugin("start", "Start the bot")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your bot. How can I assist you today? Type /list to see available commands."
    )

