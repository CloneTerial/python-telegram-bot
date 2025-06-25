from telegram import Update
from telegram.ext import ContextTypes
from Command_Handler import plugin, get_help_text

@plugin("list", "Show list commands")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   text = "list of commands:\n" + get_help_text()
   await update.message.reply_text(text)

