from Command_Handler import plugin  
from core.User_Manager import register_user, get_user

@plugin("register", "Register a new user")

async def register(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username
    full_name = update.effective_user.full_name

    if get_user(user_id):
        await update.message.reply_text("You are already registered.")
        return

    register_user(user_id, username, full_name)
    await update.message.reply_text(f"Welcome {username}! You have been successfully registered.")  