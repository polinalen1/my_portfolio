import wikipedia
import telebot
from telebot import types

token = "6783835964:AAE6eL1PVJiSffXWGkv_BoGjCRUfs6iD9Ek"

bot = telebot.TeleBot(token)

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, @{str(message.from_user.username)}!")

    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("Случайная статья")
    markup.add(item1)
    bot.send_message(message.chat.id, """
    Данный бот создан для нахождения любой статьи на Wikipedia.com.
Введи любое слово, по которому ты хочешь узнать информацию, или нажми на кнопку "Случайная статья"!""", reply_markup=markup)


@bot.message_handler(commands=["random"])
def random_page(message):
    try:
        random_page = wikipedia.random(pages=1)
        page = wikipedia.page(random_page)
        summary = wikipedia.summary(page)

        max_length = 4096
        while summary:
            bot.send_message(message.chat.id, summary[:max_length])
            summary=summary[max_length:]

        bot.send_message(message.chat.id, f"Полная статья: {page.url}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
def wiki_search(message):
    wanted_page = message.text
    try:
        page = wikipedia.summary(wanted_page)
        summary = wikipedia.summary(page)
        max_length = 4096
        while summary:
            bot.send_message(message.chat.id, summary[:max_length])
            summary = summary[max_length:]

        bot.send_message(message.chat.id, f"Полная статья: {page.url}")
    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id, "Страница не найдена.")
    except wikipedia.exceptions.DisambiguationError as e:
        options = '\n'.join(e.options)
        bot.send_message(message.chat.id, f"Запрос неоднозначный. Выберите один из вариантов:\n{options}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

@bot.message_handler(func = lambda message: True)
def search(message):
    if message.text == "Случайная статья":
        random_page(message)
    else:
        wiki_search(message)

bot.polling(none_stop=True, interval=0)