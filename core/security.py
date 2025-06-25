from core.User_Manager import get_user

def require_registration(func):
    async def wrapper(update, context):
        user_id = update.effective_user.id

        if not get_user(user_id): 
            await update.message.reply_text(
                "You need to register first. Please use /register command to register."
            )
            return
        return await func(update, context)
    return wrapper