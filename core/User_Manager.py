import json
import os
from datetime import datetime, timedelta
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/users.json"
OWNER_ID = int(os.getenv("OWNER_ID"))
transaction_path = "data/transaction.json"

# --- Utils DB ---
def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
def load_transaction():
    if not os.path.exists(transaction_path):
        return {}
    with open(transaction_path, "r") as f:
        return json.load(f)
        
def save_transaction(data):
    with open(transaction_path, "w") as f:
        json.dump(data, f, indent=2)

# --- Register User ---
def register_user(user_id, username=None, full_name=None):
    db = load_db()
    uid = str(user_id)
    now = datetime.now().isoformat()

    if uid not in db:
        db[uid] = {
            "id": user_id,
            "username": username or "",
            "full_name": full_name or "",
            "role": {
                "type": "owner" if user_id == OWNER_ID else "free",
                "expires": None if user_id == OWNER_ID else None
            },
            "registered_at": now,
            "last_active": now
        }
    else:
        db[uid]["last_active"] = now

    save_db(db)

# --- Promote User ---
def promote_user(user_id: int, role: str, duration: int, unit: str):
    db = load_db()
    uid = str(user_id)

    if uid not in db:
        return False, f"User {user_id} not found."

    now = datetime.now()
    if unit == "h":
        expires = now + timedelta(hours=duration)
    elif unit == "d":
        expires = now + timedelta(days=duration)
    else:
        return False, "Invalid time unit. Use 'h' for hours or 'd' for day."

    db[uid]["role"] = {
        "type": role,
        "expires": expires.isoformat()
    }
    save_db(db)
    return True, f"User {user_id} promoted to {role} until {expires.strftime('%Y-%m-%d %H:%M:%S')}."

# --- Demote User ---
def demote_user(user_id: int):
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        return False, f"User {user_id} not found."
    
    db[uid]["role"] = {
        "type": "free",
        "expires": None
    }
    save_db(db)
    return True, f"User {user_id} has been demoted to free user."


# --- Role Checker ---
def get_user(user_id):
    db = load_db()
    user = db.get(str(user_id), None)
    if not user:
        return None

    role_data = user.get("role", {"type": "free", "expires": None})
    role_type = role_data.get("type", "free")
    expires = role_data.get("expires")

    # Auto-demote if expired
    if role_type != "owner" and expires:
        try:
            exp_dt = datetime.fromisoformat(expires)
            if datetime.now() > exp_dt:
                user["role"] = { "type": "free", "expires": None }
                db[str(user_id)] = user
                save_db(db)
        except:
            pass
    return user

def get_role(user_id):
    user = get_user(user_id)
    if not user:
        return "unknown"
    return user["role"]["type"]

def is_premium_user(user_id):
    role = get_role(user_id)
    return role in ["premium", "owner"]

def is_store_user(user_id):
    user = get_user(user_id)
    if not user:
        return False
    return user.get("role", {}).get("type") == "store"

def is_owner_user(user_id):
    return user_id == OWNER_ID


def is_owner(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        user = get_user(user_id)

        if not user:
            await update.message.reply_text("❌ you need to register first.")
            return

        role_data = user.get("role", {"type": "free", "expires": None})
        role = role_data.get("type", "free")
        expires = role_data.get("expires")

        if role != "owner":
            await update.message.reply_text("❌ no permission, only owner can use this command.")
            return

        if expires:
            from datetime import datetime
            try:
                if datetime.fromisoformat(expires) < datetime.now():
                    await update.message.reply_text("⚠️ Your owner access has expired.")
                    return
            except:
                pass 

        return await func(update, context, *args, **kwargs)
    return wrapper

def is_premium(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        user = get_user(user_id)

        if not user:
            await update.message.reply_text("❌ you need to register first.")
            return

        role_data = user.get("role", {"type": "free", "expires": None})
        role = role_data.get("type", "free")
        expires = role_data.get("expires")

        if role not in ["premium", "owner"]:
            await update.message.reply_text("⛔ you need to be a premium user to use this command.")
            return

        if expires and role != "owner":
            try:
                if datetime.fromisoformat(expires) < datetime.now():
                    await update.message.reply_text("⚠️ Your premium access has expired.")
                    return
            except:
                pass

        return await func(update, context, *args, **kwargs)
    return wrapper

def is_store(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        user = get_user(user_id)

        if not user:
            await update.message.reply_text("❌ you need to register first.")
            return

        role_data = user.get("role", {"type": "free", "expires": None})
        role = role_data.get("type", "free")
        expires = role_data.get("expires")

        if role not in ["store", "owner"]:
            await update.message.reply_text("⛔ you need to be a store user to use this command.")
            return

        if expires and role != "owner":
            try:
                if datetime.fromisoformat(expires) < datetime.now():
                    await update.message.reply_text("⚠️ Your store access has expired.")
                    return
            except:
                pass

        return await func(update, context, *args, **kwargs)
    return wrapper
