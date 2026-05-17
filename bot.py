import telebot

# Вставьте ваш токен от @BotFather прямо сюда:
TOKEN = "8818659447:AAH-TPTnSmgCDxzJqM-h0FKmSIjC6wFJWQg"
bot = telebot.TeleBot(TOKEN)

# При команде /start просим ввести цифру
@bot.message_handler(commands=['start'])
def start_welcome(message):
    bot.reply_to(message, "Напишите цифру 13 если хотите пройти дальше")

# Проверка ввода цифры 13
@bot.message_handler(content_types=['text'])
def check_captcha(message):
    if message.text.strip() == "13":
        # Сюда пишите ваш финальный текст
        success_text = (
            "Привет! Вы успешно прошли проверку.\n"
            


"для zаKаzа мяу мяу pишиtе @videtob"
        )
        bot.reply_to(message, success_text)
    else:
        bot.reply_to(message, "Неверно. Напишите цифру 13 если хотите пройти дальше")

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
