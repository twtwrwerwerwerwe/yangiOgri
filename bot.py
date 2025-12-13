import re
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
# bu guruhlardan kelgan xabarlar umuman filtrlanmaydi
IGNORE_GROUPS = {
    -1003398571650,
    -1002963614686
}

# bu guruhlarga buyurtma yuboriladi
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
    # odam bor
    'odam bor','odambor','odam bor ekan','odam bor edi','odam borakan',
    'bitta odam bor','ikkita odam bor','uchta odam bor',"to'rtta odam bor",'tortta odam bor',
    'komplek odam bor','komplekt odam bor','kompilek odam bor','kampilek odam bor',
    '1ta odam bor','2ta odam bor','3ta odam bor','4ta odam bor',
    'odam bor 1','odam bor 2','odam bor 3','odam bor 4',
    'rishtonga odam bor','toshkentga odam bor',"toshkendan farg'onaga odam bor",
    'тўрта одам бор','одам бор','комплект одам бор','компилект odam бор','кампилек одам бор',
    'towga 1kishi', 'toshkentga 1kishi', "farg'onaga 1kishi", 'rishtonga 1kishi', '1kishi bor',
    'towga 2kishi', 'toshkentga 2kishi', "farg'onaga 2kishi", 'rishtonga 2kishi', '2kishi bor',
    'towga 3kishi', 'toshkentga 3kishi', "farg'onaga 3kishi", 'rishtonga 3kishi', '3kishi bor',
    'towga 4kishi', 'toshkentga 4kishi', "farg'onaga 4kishi", 'rishtonga 4kishi', '4kishi bor',
    'машина бор','одам бор эди','одам бор экан','одам бор 1','одам бор 2','одам бор 3','одам бор 4',
    'битта одам бор','иккита одам бор','учта одам бор','комплек одам бор','1та одам бор','2та одам бор',
    '3та одам бор','4та одам бор', 'toshkentdan bir kishi', 'rishtonga bir kishi', '1 ta qiz bor', 'ayol kishi bor mashina sorashyabdi'
    'Chirchiqdan 1 kishi', 'Yangiyuldan 1 kishi', 'Zangiotadan 1 kishi', 'Qibraydan 1 kishi', '1 kishi bor',
    '2-ta odam bor', '2-kishi bor', '3-ta odam bor', '3-kishi bor', '4-ta odam bor', '4-kishi bor',
    '2-ta kishi bor', '3-ta kishi bor', '4-ta kishi bor', '2-ta ayolkishi bor', '3-ta ayolkishi bor', '4-ta ayolkishi bor', "odam.bor", 
    
    # mashina kerak
    'mashina kerak','mashina kere','mashina kerek','mashina kera','mashina keraa',
    'bagajli mashina kerak','bosh mashina kerak','bosh mashina bormi','boshi bormi',
    'mashina izlayapman','mashina topaman','mashina kerak edi',
    'машина керак','багажли машина керак','бош машина керак','машина кере','машina кераа',

    # pochta bor
    'pochta bor','pochta kerak','pochta ketadi','pochta olib ketadi','pochta bormi',
    'почта бор','почта кетади','почта керак','почта олиб кетади',
    'тошкентга почта бор','тошкентдан почта бор','риштонга почта бор','риштондан почта бор',

    # ketadi
    'ketadi','ketvotti','ketishi kerak',
    'кетяпт','кетвотди','кетади','кетишади','кетиши керак',

    # dostavka
    'dastavka bor','dostavka bor','dastafka','dastafka bor',
    'доставкa бор','даставка бор','доставка бор','доставкa керак'
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

    # 1️⃣ ignore guruh bo‘lsa → umuman tegmaymiz
    if chat_id in IGNORE_GROUPS:
        return

    # 2️⃣ keyword bo‘lmasa → o‘tamiz
    if not match_keywords(msg.text):
        return

    # 3️⃣ xabarni o‘chiramiz
    try:
        await msg.delete()
    except:
        pass

    user = msg.from_user
    uid = str(user.id)

    phone = db.get(uid, "Raqam berkitilgan")

    # 🔗 ASL XABAR LINKI (qaysi guruhdan bo‘lsa o‘sha yerga olib boradi)
    source_link = f"https://t.me/c/{str(msg.chat.id)[4:]}/{msg.message_id}"

    safe_text = html.escape(msg.text)

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Habar manzili", url=source_link)],
        [InlineKeyboardButton(text="✅ Qabul qildim", callback_data=f"accept:{uid}")]
    ])

    text = (
        "<b>🚖 Yangi buyurtma!</b>\n\n"
        f"📝 <b>Matn:</b>\n{safe_text}\n\n"
        f"📞 <b>Raqam:</b> {phone}"
    )

    for gid in FORWARD_GROUPS:
        await bot.send_message(
            gid,
            text,
            reply_markup=buttons,
            parse_mode="HTML"
        )

# ================= QABUL QILDIM =================
@dp.callback_query(F.data.startswith("accept:"))
async def accept(cb: types.CallbackQuery):
    accepter = html.escape(cb.from_user.full_name)

    # eski matndan faqat sarlavha va raqamni qoldiramiz
    new_text = (
        "<b>🚖 Buyurtma qabul qilindi!</b>\n\n"
        "📝 <b>Matn:</b>\nBuyurtma qabul qilindi\n\n"
        f"✅ <i>{accepter} tomonidan qabul qilindi</i>"
    )

    # 🔥 XABARNI HAMMA UCHUN YANGILAYMIZ
    await cb.message.edit_text(
        new_text,
        parse_mode="HTML",
        reply_markup=None  # tugmalar o‘chadi
    )

    await cb.answer("Siz buyurtmani qabul qildingiz")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
