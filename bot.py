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
    '3та одам бор','4та одам бор', 'toshkentdan bir kishi', 'rishtonga bir kishi', '1 ta qiz bor', 'ayol kishi bor mashina sorashyabdi',
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
    'кетяпт','кетвотди','кетади','кетишади','кетиши керак', "1kishi ekan", "2kishi ekan", "3kishi ekan", "4kishi ekan",
    "2 kishi ekan", "3 kishi ekan", "1 kishi ekan", "toshketga 1kishi", "toshkenda odam bor",

    # dostavka
    'dastavka bor','dostavka bor','dastafka','dastafka bor',
    'доставкa бор','даставка бор','доставка бор','доставкa керак',
    "Toshkentdan Rishtonga 1odam bor", '1odam bor', '1ta kamla', 'bitta kamlarga', '1ta kamlarga',
    '1 ta kamlarga', '2kiwimiz', "bagajga yuk bor", '2kishimiz', "2 kiwimiz", "2 kishimiz", "2kiwimiz", 
    "3kiwimiz", "3 kiwimiz", "3 kishimiz", "3kishimiz", "4kishimiz", "4kiwimiz", "4 kishimiz", "4 kiwimiz",
    "Toshkentga 1kishi", "Toshkenga 1kishi", "Rishtonga 1kishi", "Rishotondan 1kiwi", "poshta  bor", "moshina kerak",
    "ayollar bor mashina kerak", "ayollar bor moshina kerak", "Toshkentga 1ta odam bor", "1 ta qiz bola bor", "qiz bola bor",
    "1ta qiz bor", "1ta qiz bola bor", 'одам бор',
    'одам бор экан','одам бор эди','битта одам бор','иккита одам бор','учта одам бор','тўртта одам бор','1та одам бор','2та одам бор','3та одам бор','4та одам бор','одам бор 1','одам бор 2','одам бор 3','одам бор 4',

    'комплек одам бор','комплект одам бор','компилек одам бор','кампилек одам бор',

    'риштонга одам бор','тошкентга одам бор','тошкентдан фарғонага одам бор','тошкентга 1 киши','риштонга 1 киши','фарғонага 1 киши','1 киши бор','2 киши бор','3 киши бор','4 киши бор',
    'чирчиқдан 1 киши', 'янгийўлдан 1 киши', 'зангиотадан 1 киши', 'қибрайдан 1 киши',

    '1 та қиз бор', '1 та қиз бола бор', 'қиз бола бор', 'аёл киши бор машина сўрашяпти', 'аёллар бор машина керак',

    # mashina
    'машина керак', 'машина кере', 'машина керeк', 'багажли машина керак', 'машина излаяпман', 'мошина керак',

    # pochta / dostavka
    'почта бор', 'почта керак', 'почта олиб кетади', 'пошта бор', 'даставка бор', 'доставка бор',

    # ketadi
    'кетади', 'кетвотти', 'кетиши керак', "shopir kerak", "1kishi ayol kishili mashina kerak", 
    "gazalkentdan 1kishi", "g'azalkentdan 1kishi", "gazalkentdan 2kishi", "g'azalkantdan 2 kishi",
    "o'zimizdan 1kishi", "ozimizdan 1kishi", "ozimizdan 2 kishi", "ozimizdan kim bor", "o'zimizdan kim bor",
    "yengil mashina kerak", "amirsoydan 1kishi", "qoqonga 1kishi", "kim yurapti akalar", "pustoy mashina kerak",
    "kobalt kerak", "jentra kerak", "bosh mashina bormi", "uchkoprikda 1kishi", "uchkoprikdan 1kishi", "chirchiqdan 1kishi",
    "yangiqorgondan 1kishi", "tashkentdan rishtonga odam bor", "toshkendan bog'dodga odam bor", "toshkentdan bagdodga odam bor",
    "4 odam bor", "2ta ayol bor", "katta yoshli ayol bor", "bir qiz bir bola bor", "srochni yuradigan taxi kerak",
    "kim yuryabdi", "toshkentga ketaman", "bagdodga ketishi kerak", "bagdodan 1kishi bor", "bog'doddan 2kishi",
    'кетади', 'кетвотти', 'кетиши керак', "шопир керак", "1киши аёл кишили машина керак",
    "газалкентдан 1киши", "ғазалкентдан 1киши", "газалкентдан 2киши", "ғазалкентдан 2 киши",
    "ўзимиздан 1киши", "озимиздан 1киши", "озимиздан 2 киши", "озимиздан ким бор", "ўзимиздан ким бор",
    "енгил машина керак", "амирсойдан 1киши", "қўқонга 1киши", "ким юрапти акалар", "пустой машина керак",
    "кобальт керак", "джентра керак", "бош машина борми", "учкўприкда 1киши", "учкўприкдан 1киши", "чирчиқдан 1киши",
    "янгиқўрғондан 1киши", "ташкентдан риштонга одам бор", "тошкентдан боғдодга одам бор", "тошкентдан бағдодга одам бор",
    "4 одам бор", "2та аёл бор", "катта ёшли аёл бор", "бир қиз бир бола бор", "срочни юрадиган такси керак",
    "ким юряпти", "тошкентга кетаман", "бағдодга кетиши керак", "бағдодан 1киши бор", "боғдоддан 2киши",
    "qoqonga odam bor", "qoqondan odam bor", "ertagaga qoqonga 1kishi", "fargonadan 1kishi", 'fargonaga odam bor',
    "fargonaga kim yuryabdi", "fargonaga 2kishi", "қўқонга одам бор", "қўқондан одам бор", "эртагага қўқонга 1киши", "фарғонадан 1киши", 'фарғонага одам бор',
    "фарғонага ким юряпти", "фарғонага 2киши"
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

    # 👤 USER MENTION
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

    # 📨 MENTION XABAR
    notify_msg = await bot.send_message(
        chat_id=chat_id,
        text=(
            f"{mention}\n\n"
            "✅ <b>Buyurtmangiz qabul qilindi!</b>\n"
            "🚖 Shofyor tez orada siz bilan aloqaga chiqadi."
        ),
        parse_mode="HTML"
    )

    # ⏱ 5 SONIYADAN KEYIN O‘CHIRAMIZ
    await asyncio.sleep(5)
    try:
        await notify_msg.delete()
    except:
        pass

    # ================= BUYURTMA YUBORISH =================
    phone = db.get(uid, "Raqam berkitilgan")
    safe_text = html.escape(msg.text)

    profile_link = (
        f"https://t.me/{user.username}"
        if user.username else f"tg://user?id={user.id}"
    )

    # 👤 PROFIL BUTTON
    if user.username:
        profile_url = f"https://t.me/{user.username}"
    else:
        profile_url = f"tg://user?id={user.id}"

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profil", url=profile_url)],
        [InlineKeyboardButton(text="✅ Qabul qildim", callback_data=f"accept:{user.id}")]
    ])



    order_text = (
        "<b>🚖 Yangi buyurtma!</b>\n\n"
        f"📝 <b>Matn:</b>\n{safe_text}\n\n"
        f"📞 <b>Raqam:</b> {phone}"
    )

    for gid in FORWARD_GROUPS:
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
