import telebot
import sqlite3
from telebot import types

TOKEN = "8535821276:AAGG-w2qWgpE8SlxjuLZQpqOYPWFGxX1m8E"
ADMIN_USERNAME = "@sonyapro1"   # человек, которому пишут
ADMIN_ID = 8146320391           # твой Telegram ID (для уведомлений)

bot = telebot.TeleBot(TOKEN)

# ================== БАЗА ДАННЫХ ==================
conn = sqlite3.connect("keys.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    used INTEGER DEFAULT 0
)
""")
conn.commit()

# ================== ГЛАВНОЕ МЕНЮ ==================
def main_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🛒 Купить ключ", url=f"tg://resolve?domain={ADMIN_USERNAME[1:]}"),
    )
    kb.add(
        types.InlineKeyboardButton("🔑 Ввести ключ", callback_data="enter_key")
    )
    kb.add(
        types.InlineKeyboardButton("ℹ Поддержка", url=f"tg://resolve?domain={ADMIN_USERNAME[1:]}")
    )
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "<b>Добро пожаловать в магазин ключей!</b>\n\n"
        "Чтобы купить ключ, нажмите кнопку ниже или напишите создателю.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ================== CALLBACK ==================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "enter_key":
        msg = bot.send_message(call.message.chat.id, "🔑 Введите ваш ключ:")
        bot.register_next_step_handler(msg, check_key)

# ================== ПРОВЕРКА КЛЮЧА ==================
def check_key(message):
    user_key = message.text.strip()

    cursor.execute("SELECT id, used FROM keys WHERE code=?", (user_key,))
    result = cursor.fetchone()

    if result is None:
        bot.send_message(message.chat.id, "❌ Ключ не найден. Проверьте правильность ввода.")
        return

    key_id, used = result

    if used == 1:
        bot.send_message(message.chat.id, "⚠ Этот ключ уже был использован ранее.")
        return

    # Отмечаем ключ как использованный
    cursor.execute("UPDATE keys SET used=1 WHERE id=?", (key_id,))
    conn.commit()

    bot.send_message(message.chat.id, "✅ Ключ успешно активирован!")

    # Уведомление админу
    try:
        bot.send_message(
            ADMIN_ID,
            f"🔔 <b>ПОЛЬЗОВАТЕЛЬ АКТИВИРОВАЛ КЛЮЧ</b>\n\n"
            f"👤 ID: {message.from_user.id}\n"
            f"🔑 Ключ: <code>{user_key}</code>",
            parse_mode="HTML"
        )
    except:
        pass

# ================== ЗАПУСК ==================
bot.infinity_polling()
