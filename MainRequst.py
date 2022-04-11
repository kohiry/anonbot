import requests
from info import setting

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


conn = sqlite3.connect('BASE.db', check_same_thread=False)
cur = conn.cursor()
#DATA_ID = cur.execute('SELECT userid FROM users')
local_user = ''


users_pair = {
"1": "1"
 #"644823883": "994185429",
 #"994185429": "644823883"
 #"997740537": "644823883"
}

offset = 0 # for added up to date

def create_request(chat_id, text, parse_mode='HTML'):
    URL = 'https://api.telegram.org/bot'
    TOKEN = setting
    message_data = { #create requests for send message
    'chat_id': chat_id,
    'text': text,
    #'reply_to_message_id': update['message']['message_id'], # sendo to reply?? wtf
    'parse_mode': parse_mode # about formate text down
    }
    try:
        request = requests.post(URL+TOKEN+'/sendMessage', data=message_data)
    except:
        print('Error')
        return False
    finally:
        #if not request.status_code == 200:
        #    return 200
        #else:
        print('Succeseful')
        return request


def check_update():
    global offset

    URL = 'https://api.telegram.org/bot'
    TOKEN = setting
    DATA = {'offset': offset + 1, 'limit':0, 'timeout': 0}

    try:
        request = requests.get(URL+TOKEN+'/getUpdates', data=DATA)
    except Exception as e:
        print("Error Lol", e)
        return False
    if not request.status_code == 200:
        return False
    if not request.json()['ok']:
        return False

    for update in request.json()['result']:
        offset = update['update_id'] # подтверждаем обновление
        if 'message' not in update or 'text' not in update['message']: # this is not mesage?
            print('wtf is it')
            continue
        elif str(update['message']['chat']['id']) in list(users_pair.keys()): # не проверено, работает ли
            bot.send_message(users_pair[str(update['message']['chat']['id'])], update['message']['text'])
        if  '/start' in update['message']['text']:
            reg_commit = local_user.registration()
            if reg_commit == "Added":
                create_request(update['message']['chat']['id'], 'Новичок, это хорошо!')
            elif reg_commit == "Been":
                create_request(update['message']['chat']['id'], 'Ты уже зарегистрирован.')
        create_request(update['message']['chat']['id'], 'Sup')




while True:
    try:
        check_update()
    except KeyboardInterrupt: # if I stop bot
        print('bb')
        break
