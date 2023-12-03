import telebot
from telebot import types
import random

token = "6645452788:AAFXSUjM0OTtVSIqkN4lSJjPnCHg_AYP3o0"

bot = telebot.TeleBot(token)


class IncrementCounter:

    def __init__(self):
        self._value = 0

    def new_value(self):
        self._value += 1
        return self._value
    def last_value(self):
        return self._value

counter1 = IncrementCounter()
counter2 = IncrementCounter()

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет. Давай сыграем в камень-ножницы-бумага.")
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Камень")
    item2=types.KeyboardButton("Ножницы")
    item3=types.KeyboardButton("Бумага")
    item4 = types.KeyboardButton("Закончить игру")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id,  "Начинай игру. Выбирай!", reply_markup=markup)


@bot.message_handler(content_types = ["text"])
def answer(message):
    if message.text == "Закончить игру":
        bot.send_message(message.chat.id, f"Игра закончена. Итоговый счёт: {counter1.last_value()} : {counter2.last_value()}.")
        counter1.__init__()
        counter2.__init__()
        bot.send_message(message.chat.id, "Если снова захочешь поиграть, просто выбери - камень, ножницы или бумагу!")
    else:
        answers=["Камень", "Ножницы", "Бумага"]
        bot_answer= random.choice(answers)
        bot.send_message(message.chat.id, bot_answer)

        if (message.text=="Камень" and bot_answer=="Ножницы") or \
                (message.text=="Ножницы" and bot_answer=="Бумага") or \
                (message.text=="Бумага" and bot_answer=="Ножницы"):
            bot.send_message(message.chat.id, "Ты победил! "+f"Счёт: {counter1.new_value()} : {counter2.last_value()}")
        elif message.text==bot_answer:
            bot.send_message(message.chat.id, "Ничья!")
        else:
            bot.send_message(message.chat.id, "Бот победил! "+f"Счёт: {counter1.last_value()} : {counter2.new_value()}")



bot.polling(none_stop=True, interval=0)