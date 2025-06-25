from Command_Handler import plugin
from core.User_Manager import is_owner, promote_user


@plugin("promote", "Promote a user to a specific role with an expiration time")
@is_owner  
    
async def promote(update, context):
    args = context.args
    if len(args) != 4:
        await update.message.reply_text("Usage: /promote <user_id> <role> <duration> <unit>")
        return
    
    try:
        user_id = int(args[0])
        role = args[1]
        duration = int(args[2])
        unit = args[3]
    except:
        await update.message.reply_text("Invalid arguments. Please check your input.")
        return
    
    ok, msg = promote_user(user_id, role, duration, unit)
    if ok:
        await update.message.reply_text(f"User {user_id} has been promoted to {role} for {duration} {unit}.")