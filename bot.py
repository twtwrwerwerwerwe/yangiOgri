import json
import html
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

# ================= TOKEN =================
TOKEN = "7990459607:AAHabwIyHWo5e01xfpP79vrL-RpNWm1OlyA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================= GURUHLAR =================
IGNORE_GROUPS = {
    -1003398571650,
    -1002963614686
}

FORWARD_GROUPS = [
    -1003398571650,
    -1002963614686
]

# ================= DATABASE =================
DB_FILE = "users.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

db = load_db()

# ================= KEYWORDS =================
KEYWORDS = [
    "odam bor", "mashina kerak", "pochta bor",
    "ketadi", "dostavka bor",
    "одам бор", "машина керак", "почта бор"
]

def match_keywords(text: str) -> bool:
    text = text.lower()
    return any(k in text for k in KEYWORDS)

# ================= /start =================
@dp.message(F.text == "/start")
async def start(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await msg.answer(
        "Assalomu alaykum!\n\nTelefon raqamingizni yuboring 👇",
        reply_markup=kb
    )

# ================= CONTACT =================
@dp.message(F.contact)
async def save_contact(msg: types.Message):
    db[str(msg.from_user.id)] = msg.contact.phone_number
    save_db(db)

    await msg.answer(
        "✅ Raqamingiz saqlandi",
        reply_markup=types.ReplyKeyboardRemove()
    )

# ================= FILTR =================
@dp.message(F.text)
async def filter_messages(msg: types.Message):
    chat_id = msg.chat.id

    if chat_id in IGNORE_GROUPS:
        return

    if not match_keywords(msg.text):
        return

    user = msg.from_user
    uid = str(user.id)

    # 🔹 USER PROFILE LINK
    if user.username:
        profile_link = f"https://t.me/{user.username}"
    else:
        profile_link = f"tg://user?id={user.id}"

    # 🔹 USER MENTION TEXT
    if user.username:
        mention = f"@{user.username}"
    else:
        safe_name = html.escape(user.full_name)
        mention = f'<a href="tg://user?id={user.id}">{safe_name}</a>'

    # 🔥 ASL XABARNI O‘CHIRAMIZ
    try:
        await msg.delete()
    except:
        pass

    # 📨 ASL GURUHDA BUYURTMA QABUL QILINDI DEYISH
    notify_msg = await bot.send_message(
        chat_id=chat_id,
        text=(
            f"{mention}\n\n"
            "✅ <b>Buyurtmangiz qabul qilindi!</b>\n"
            "🚖 Shofyor tez orada siz bilan aloqaga chiqadi."
        ),
        parse_mode="HTML"
    )

    # ================= BUYURTMA FORWARD QILISH =================
    phone = db.get(uid, "Raqam berkitilgan")
    safe_text = html.escape(msg.text)

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profil", url=profile_link)],
        [InlineKeyboardButton(text="✅ Qabul qildim", callback_data=f"accept:{uid}")]
    ])

    order_text = (
        "<b>🚖 Yangi buyurtma!</b>\n\n"
        f"📝 <b>Matn:</b>\n{safe_text}\n\n"
        f"📞 <b>Raqam:</b> {phone}"
    )

    for gid in FORWARD_GROUPS:
        # FORWARD QILGAN XABAR USTIDA PROFIL TUGMASI
        await bot.send_message(
            gid,
            order_text,
            reply_markup=buttons,
            parse_mode="HTML"
        )


# ================= QABUL QILDIM =================
@dp.callback_query(F.data.startswith("accept:"))
async def accept(cb: types.CallbackQuery):
    accepter = html.escape(cb.from_user.full_name)

    new_text = (
        "<b>🚖 Buyurtma qabul qilindi!</b>\n\n"
        f"✅ <i>{accepter} tomonidan qabul qilindi</i>"
    )

    await cb.message.edit_text(
        new_text,
        parse_mode="HTML",
        reply_markup=None
    )

    await cb.answer("Buyurtma sizga biriktirildi")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
