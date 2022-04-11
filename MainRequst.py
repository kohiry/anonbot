import requests
from info import setting
from random import choice
import sqlite3


CONDITION = 'SEARCH' #'SEARCH, TALK'

class Anonims:
    def __init__(self, id):
        self.id = id
        self.conn = sqlite3.connect('BASE.db', check_same_thread=False)
        self.cur = self.conn.cursor()

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
            return list(one_result)
        elif len(one_result) < 2:
            return 'NULL'

    def clear_queue(self):
        self.cur.execute("DELETE FROM queue")
        self.conn.commit()

    def add_queue(self): # True - wanna talk in condition - seeker, false - did't want
        self.add_into_base(f"INSERT INTO queue VALUES({int(self.id)});")


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


def pairs_transform():
    dict_pairs = dict()
    with open('Pairs.txt', 'r') as f:
        pair_data = f.readlines()
    for line in pair_data:
        first, second = line.split(';')[0], line.split(';')[1]
        dict_pairs[first[0]] = first[1]
        dict_pairs[first[1]] = first[0]
        dict_pairs[second[0]] = second[1]
        dict_pairs[second[1]] = second[0]
        print(first,second)
    return dict_pairs


def check_update():
    global offset, local_user


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
        try:
            print(request.json())
            offset = update['update_id'] # подтверждаем обновление
            if 'edited_message' not in update:
                local_user = Anonims(update['message']['chat']['id']) #Бот ложится, если изменить одно из сообщений
                answer = local_user.want_search()
                print(pairs_transform(), 'check')
                if type(answer) == type([]):
                    print('Nice', answer)
                    with open('Pairs.txt', 'a') as f:
                        f.write(str(answer[0][0]) + '=' + str(answer[1][0]) + ';' + str(answer[1][0]) + '=' + str(answer[0][0])+'\n')
                    local_user.clear_queue()
                if 'message' not in update or 'text' not in update['message']: # this is not mesage?
                    print('wtf is it')
                    continue
                elif '/search' in update['message']['text']:
                    local_user.add_queue()
                elif str(update['message']['chat']['id']) in list(users_pair.keys()): # не проверено, работает ли
                    create_request(users_pair[str(update['message']['chat']['id'])], update['message']['text'])
                if  '/start' in update['message']['text']:
                    reg_commit = local_user.registration()
                    if reg_commit == "Added":
                        create_request(update['message']['chat']['id'], 'Новичок, это хорошо!')
                    elif reg_commit == "Been":
                        create_request(update['message']['chat']['id'], 'Ты уже зарегистрирован.')
                create_request(update['message']['chat']['id'], 'Sup')
        except Exception as e:
            print(e, 'Bag ignor')



while True:
    try:
        check_update()
    except KeyboardInterrupt: # if I stop bot
        print('bb')
        break
