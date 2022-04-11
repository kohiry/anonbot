import telebot
from info import setting
from telebot import types
from random import choice
import sqlite3


CONDITION = 'SEARCH' #'SEARCH, TALK'

class Anonims:
    def __init__(self, id):
        self.id = id
        self.conn = sqlite3.connect('BASE.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.good_data = [] # id status True

    def add_into_base(self, sqlite_insert_query, test=False):
        self.cur.execute(sqlite_insert_query)
        if not test:
            self.conn.commit()

    def all_user(self):
        self.cur.execute(f"SELECT userid, status FROM users")
        one_result = self.cur.fetchall()
        return one_result

    def want_search(self):
        self.cur.execute(f"SELECT userid FROM queue")
        one_result = self.cur.fetchall()
        if len(one_result) >= 2:
            return one_result
        elif len(one_result) < 2:
            return 'NULL'

    def find_good(self): # True - wanna talk in condition - seeker, false - did't want
        list_users = self.all_user()
        self.good_data = [i[0] for i in list_users if i[1] == 1 and i[0] != self.id] # find free users; 1== free 0= not


    def find_pair(self, id):
        while True:
            self.find_good()
            if len(self.good_data) != 0:
                self.friend_id = choice(self.good_data)
                break

    def registration(self): # test используется выше чтобы не коммитить пользователя
        # проверка есть ли userid в таблице users
        info = self.cur.execute('SELECT userid FROM users WHERE userid=?', (int(self.id),))
        if info.fetchone() is None:
            # если человека нету в бд
            none_team = "noneteam"
            self.add_into_base(f"INSERT INTO users VALUES({int(self.id)}, 0);")
            return "Added"
        else:
            # если человек есть в бд
            return "Been"


class User:
    def __init__(self, id, status=False):
        self.status = status # True/False
        self.id = id
        self.friend_id = 0

    def change_status(self, status):
        self.status = status


conn = sqlite3.connect('BASE.db', check_same_thread=False)
cur = conn.cursor()
#DATA_ID = cur.execute('SELECT userid FROM users')
local_user = ''

# Инициализация бота и основные обработчики комманд,основная логика в Obj
bot = telebot.TeleBot(setting);

users_pair = {
"1": "1"
 #"644823883": "994185429",
 #"994185429": "644823883"
 #"997740537": "644823883"
}

@bot.callback_query_handler(func=lambda call: call.data == 'cbTeam1')
def cb_buttonTeam1(message: types.Message):
    pass


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    global local_user, CONDITION

    if CONDITION == 'SEARCH':
        local_user = Anonims(message.from_user.id)
        answer = local_user.want_search()
        if type(answer) == type([]):
            print('Nice')
            CONDITION = "TALK"
    elif CONDITION == 'TALK':
        if message.text in ["Привет", "привет", "сап", "s"]:
            bot.send_message(message.from_user.id, message.from_user.id)
        elif str(message.from_user.id) in list(users_pair.keys()):
            bot.send_message(users_pair[str(message.from_user.id)], message.text)
        elif "/start" in message.text:
            reg_commit = local_user.registration()
            if reg_commit == "Added":
                bot.send_message(message.from_user.id, 'Новичок, это хорошо!')
            elif reg_commit == "Been":
                bot.send_message(message.from_user.id, "Ты уже зарегистрирован.")




bot.polling(none_stop=True, interval=0)
