from telegram import Update
from telegram.ext import ContextTypes
from Command_Handler import plugin  

@plugin("id", "Get your user ID")
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your user ID is: {user.id}")