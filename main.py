import telebot
import wikipedia
import re
import os

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Устанавливаем украинский язык Википедии
wikipedia.set_lang("uk")


# Функция получения текста из Википедии
def getwiki(s):
    try:
        page = wikipedia.page(s)

        # Получаем первые 1000 символов
        wikitext = page.content[:1000]

        # Разделяем по точкам
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]

        wikitext2 = ""

        for x in wikimas:
            if "==" not in x:
                if len(x.strip()) > 3:
                    wikitext2 += x.strip() + "."
            else:
                break

        # Убираем разметку
        wikitext2 = re.sub(r'\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub(r'\{[^\{\}]*\}', '', wikitext2)

        return wikitext2

    except:
        return "У Вікіпедії немає інформації про це."


# ------------------------------
#        /start
# ------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "<b>👋 Привіт! Ласкаво просимо до WikiBot</b>\n\n"
        "🔎 <i>Я можу знаходити короткі та зрозумілі статті з Вікіпедії.</i>\n\n"
        "📝 Просто надішли мені будь-яке слово чи назву — і я знайду інформацію.\n\n"
        "Наприклад:\n"
        "💠 <code>Київ</code>\n"
        "💠 <code>Сонце</code>\n"
        "💠 <code>Динозаври</code>\n\n"
        "📚 Готовий дізнатися щось нове? Напиши запит!"
    )

    bot.send_message(message.chat.id, text, parse_mode='HTML')


# ------------------------------
#        /info
# ------------------------------
@bot.message_handler(commands=['info'])
def info(message):
    text = (
        "🌟 *Інформація про автора* 🌟\n\n"
        "Привіт! Я — *Alex*, автор цього бота.\n"
        "Якщо маєш питання — напиши:\n"
        "👉 https://t.me/alexkhalus\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# ------------------------------
#        /help
# ------------------------------
@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = (
        "📖 *Доступні команди:*\n\n"
        "• /info — інформація про автора\n"
        "• /start — запуск бота\n"
        "• /help — список команд\n"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# ------------------------------
#    Обработка текста от юзера
# ------------------------------
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))


# Запуск бота
bot.polling(none_stop=True)


