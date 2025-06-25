from Command_Handler import plugin
from core.User_Manager import is_owner, demote_user

@plugin("demote", "demote a user to a free user")
@is_owner

async def demote(update, context):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage: /demote <user_id>")
        return
    
    try:
        user_id = int(args[0])
    except:
        await update.message.reply_text("Invalid user ID. Please provide a valid user ID.")
        return
    
    ok, msg = demote_user(user_id)
    if ok:
        await update.message.reply_text(f"User {user_id} has been successfully demoted.")