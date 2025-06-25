from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, welcome to the bot!')

hello_handler = CommandHandler("hello", hello)
