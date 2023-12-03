import telebot
import datetime
from datetime import datetime

token = "6877804656:AAF79Vc8k7fmXAirt7WwC0kKbtnU74EpHEU"
bot = telebot.TeleBot(token)

user = {}

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, f"""Привет, @{message.from_user.username}!
Данный бот создан для отслеживания длительности и качества твоего сна, а также заметок про него!
Используй команды /sleep, /wake, /quality и /notes.""")

@bot.message_handler(commands = ["sleep"])
def sleep(message):
    forward_date = datetime.now()
    user_id = message.from_user.id
    user[user_id] = {"start_time" : forward_date}
    bot.send_message(message.chat.id, "Засек время сна! Спокойной ночи!")


@bot.message_handler(commands = ["wake"])
def wake(message):
    forward_date_wake = datetime.now()
    user_id = message.from_user.id
    data = user.get(user_id)
    if data and "start_time" in data:
        start_time = data["start_time"]
        duration = (forward_date_wake-start_time).total_seconds()/60
        data["duration"] = duration
        bot.send_message(message.chat.id, f"Продолжительность сна составила {duration:.2f} минут(ы). Не забудь оценить \
качество сна командой /quality и оставить заметки командой /notes")
    else:
        bot.send_message(message.chat.id, "Для начала отправьте команду /sleep!")

@bot.message_handler(commands = ["quality"])
def quality(message):
    try:
        quality = int(message.text.split()[1])
        user_id = message.from_user.id
        data = user.get(user_id)
        if 1 <= quality <= 10:
            if data and "duration" in data:
                data["quality"] = quality
                bot.reply_to(message, "Оценка качества учтена!")
            elif data and "duration" not in data:
                bot.send_message(message.chat.id, "Сначала нужно вычислить продолжительность сна, отправьте \
команду /wake!")
            else:
                bot.send_message(message.chat.id, "Для начала отправьте команду /sleep!")
        else:
            bot.send_message(message.chat.id, "Оценка качества должна быть цифрой от 1 до 10!")
    except ValueError:
        bot.send_message(message.chat.id, "Отправьте цифру от 1 до 10.")
    except IndexError:
        bot.send_message(message.chat.id, "Введите цифру после команды /quality.")

@bot.message_handler(commands=["notes"])
def notes(message):
    note = message.text.split("/notes", 1)[1].strip()
    user_id = message.from_user.id
    data = user.get(user_id)
    if note:
        if data and "duration" in data:
            data["notes"] = note
            bot.reply_to(message, "Заметка учтена!")
        elif data and "duration" not in data:
            bot.send_message(message.chat.id, "Сначала нужно вычислить продолжительность сна, отправьте \
команду /wake!")
        else:
            bot.send_message(message.chat.id, "Для начала отправьте команду /sleep!")
    else:
        bot.send_message(message.chat.id, "Введите заметку после команды /notes.")


bot.polling(none_stop=True, interval=0)
