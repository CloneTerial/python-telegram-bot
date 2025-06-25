from core.User_Manager import load_db, save_db, load_transaction, save_transaction, is_store
from Command_Handler import plugin
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler
from core.transactionID import generate_transaction_id
from datetime import datetime


@plugin("create_store", "Create a new store")
@is_store

async def create_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /create_store <name> <description>")
        return

    user_id = str(update.effective_user.id)
    name = args[0]
    description = " ".join(args[1:])

    db = load_db()

    if user_id not in db:
        await update.message.reply_text("User not registered.")
        return

    if "store" in db[user_id]:
        await update.message.reply_text("You already have a store.")
        return

    db[user_id]["store"] = {
        "name": name,
        "description": description,
        "producks": []
    }

    save_db(db)
    await update.message.reply_text(f"Store '{name}' created successfully with description '{description}'.")


@plugin("create_produck", "Create a new produck")
@is_store

async def create_produck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Usage: /create_produck <name> <price> <description>")
        return

    user_id = str(update.effective_user.id)
    db = load_db()

    if user_id not in db or "store" not in db[user_id]:
        await update.message.reply_text("You don't have a store. Use /create_store first.")
        return

    name = args[0]
    try:
        price = float(args[1])
    except ValueError:
        await update.message.reply_text("Price must be a number.")
        return

    description = " ".join(args[2:])

    produck = {
        "name": name,
        "price": price,
        "description": description
    }

    db[user_id]["store"]["producks"].append(produck)
    save_db(db)

    await update.message.reply_text(
        f"Product '{name}' created successfully at price {price} with description '{description}'."
    )


@plugin("buy", "Buy produck from another store")
@is_store

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /buy <store_name>")
        return
    
    store_name = args[0].lower()
    found = False
    
    for uid, data in db.items():
        store = data.get("store")
        
        if store and store.get("name", "").lower() == store_name:
            found = True
            producks = store.get("producks", [])
            
            if not producks:
                await update.message.reply_text("Store has no producks available.")
                return
            for i, p in enumerate(producks):
                text = f"📦 *{p['name']}*\n💰 Price: Rp{p['price']:.0f}\n📝 {p['description']}"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🛒 Buy", callback_data=f"buy|{uid}|{i}")]
                ])
                await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
            break
  
    if not found:
        await update.message.reply_text("Store not found.")
        
async def handle_buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    db = load_db()
    data = query.data.split("|")

    if len(data) != 3:
        await query.edit_message_text("Data rusak.")
        return

    _, seller_uid, prod_index = data
    prod_index = int(prod_index)

    seller_data = db.get(seller_uid)
    if not seller_data or not seller_data.get("store"):
        await query.edit_message_text("Toko tidak ditemukan.")
        return

    producks = seller_data["store"].get("producks", [])
    if prod_index >= len(producks):
        await query.edit_message_text("Produk tidak ditemukan.")
        return

    produck = producks[prod_index]
    pembeli = update.effective_user
    transaction_id = generate_transaction_id()
    buyer_id = str(pembeli.id)

    await query.edit_message_text(
        f"✅ *{pembeli.first_name}*, kamu membeli *{produck['name']}* seharga Rp{produck['price']:.0f} dari *{seller_data['store']['name']}* dengan id transaksi *{transaction_id}*.",
        parse_mode="Markdown"
    )
    transactions = load_transaction()
    if buyer_id not in transactions:
        transactions[buyer_id] = []

    data_transaction = {
        "id": transaction_id,
        "buyer_id": pembeli.id,
        "date": datetime.now().isoformat(),
        "seller_id": seller_uid,
        "store_name": seller_data["store"]["name"],
        "produck": produck["name"],
        "price": produck["price"]
    }

    transactions[buyer_id].append(data_transaction)
    save_transaction(transactions)
    

@plugin("produck", "View your producks")
@is_store

async def produck_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    db = load_db()

    if user_id not in db or "store" not in db[user_id]:
        await update.message.reply_text("You don't have a store. Use /create_store first.")
        return

    producks = db[user_id]["store"].get("producks", [])

    if not producks:
        await update.message.reply_text("You have no producks. Use /create_produck to create one.")
        return

    response = f"📦 Your Producks in '{db[user_id]['store']['name']}':\n"
    for i, p in enumerate(producks, start=1):
        response += f"{i}. {p['name']} - Rp{p['price']}\n   {p['description']}\n"

    await update.message.reply_text(response)
    
@plugin("my_orders", "Lihat daftar pesanan kamu")
@is_store

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    transactions = load_transaction()

    if user_id not in transactions or not transactions[user_id]:
        await update.message.reply_text("📭 Kamu belum pernah melakukan transaksi.")
        return

    # Ambil semua transaksi user
    history = transactions[user_id]
    reply = "📦 *Riwayat Pesanan Kamu:*\n"

    for i, tx in enumerate(history, start=1):
        reply += (
            f"\n{i}. 🛒 *{tx['produck']}* - Rp{tx['price']:.0f}\n"
            f"   🏪 {tx['store_name']} | ID: `{tx['id']}`\n"
            f"   🕒 {tx['date'][:19].replace('T', ' ')}\n"
        )

    await update.message.reply_text(reply, parse_mode="Markdown")
