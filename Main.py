import telebot
from info import setting
from telebot import types

# Инициализация бота и основные обработчики комманд,основная логика в Obj
bot = telebot.TeleBot(setting);

users = {
 "644823883": "644823883",
 "1": "644823883"
}

@bot.callback_query_handler(func=lambda call: call.data == 'cbTeam1')
def cb_buttonTeam1(message: types.Message):
    pass


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    print(list(users.keys()), [str(message.from_user.id)])
    if message.text in ["Привет", "привет", "сап", "s"]:
        bot.send_message(message.from_user.id, message.from_user.id)
    if "1" in message.text:
        bot.send_message(users["1"], "Good work")
    elif str(message.from_user.id) in list(users.keys()):
        bot.send_message(users[str(message.from_user.id)], "Work")

bot.polling(none_stop=True, interval=0)
