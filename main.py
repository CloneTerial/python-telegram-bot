from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler
from dotenv import load_dotenv
import importlib.util
from Command_Handler import get_handlers
import os
import logging
from plugins.store import handle_buy_callback


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_plugins(folder="plugins"):
    for file in os.listdir(folder):
        if file.endswith(".py") and not file.endswith("__init__.py"):
            path = os.path.join(folder, file)
            name = file[:-3]
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"Loaded plugin: {name}")
    

load_dotenv()
TOKEN = os.getenv("token")


app = ApplicationBuilder().token(TOKEN).build()


load_plugins("plugins") 

for handler in get_handlers():
    app.add_handler(handler)
    

app.add_handler(CallbackQueryHandler(handle_buy_callback, pattern=r"^buy\|"))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()