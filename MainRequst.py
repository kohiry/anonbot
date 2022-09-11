import requests
from info import setting, geo, town
from random import choice
import sqlite3
import traceback
from os import remove
import json
from datetime import datetime
import bad_phrase_in_dialog

users_pair = {
 '1': '1'
 #"644823883": "994185429",
 #"994185429": "644823883"
 #"997740537": "644823883"
}


class Anonims:
    def __init__(self, id):
        self.id = id
        self.new_status = 'None' # Pair/None
        self.old_status = 'None'
        self.conn = sqlite3.connect('BASE.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    def spam_control(self): # если нету id в файле добавить
        been = False
        with open("spam.txt", "r") as f:
            pair_id_spambool = tuple(f.readlines())
            print(pair_id_spambool)

        with open("spam.txt", "a") as f:
            if str(self.id)+"\n" not in pair_id_spambool:
                f.write(str(self.id)+'\n')
                print(self.id, "Нету в базе спама")
                been = True
        if been:
            return True
        else:
            print(self.id, "уже в базе спама")
            return False


    def alg_sort(self, massive):
        id_plus_keys = dict()
        for id in massive:
            id_plus_keys[id[0]] = tuple(self.cur.execute(f"SELECT black_list FROM users WHERE userid={id[0]}").fetchall())[0][0]
        return id_plus_keys


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

    def clear_queue(self, *ids):
        self.cur.execute(f"DELETE FROM queue WHERE userid={ids[0]}")
        self.cur.execute(f"DELETE FROM queue WHERE userid={ids[1]}")
        self.conn.commit()

    def checkPairs(self):
        with open('Pairs.txt', 'r') as f:
            for line in tuple(f.readlines()):
                if str(self.id) in line:
                    return False
            else:
                return True

    def upd_coord(self, latitude, longitude):
        self.add_into_base(f"UPDATE users SET coord='{latitude}%{longitude}' WHERE userid={int(self.id)};")

    def check_coord(self):
        info = self.cur.execute(f"SELECT coord FROM users WHERE userid={int(self.id)}").fetchone()
        self.conn.commit()
        return info[0]


    def add_queue(self):
        if self.checkPairs():
            self.add_into_base(f"INSERT OR IGNORE INTO queue VALUES({int(self.id)});")
        else:
            print('We have this id in base')

    def clear_solo_queue(self):
        self.cur.execute(f"DELETE FROM queue WHERE userid={int(self.id)}")
        self.conn.commit()
        print('АУАУАУА')


    def stop(self, user2_id: str):
        text = ''
        new_text = ''
        with open('Pairs.txt', 'r') as f:
            text = tuple(f.readlines())
        for line in text:
            if user2_id not in line:
                new_text += line
        with open('Pairs.txt', 'w') as f:
            f.write(new_text)
        if self.checkPairs():
            # add in black list\
            def BlackL_txt_file_costil(information, id):
                text_bl = ''
                with open('data_bl.txt', 'w') as f:
                    f.write(':'.join([i[0] for i in information.fetchall()]))
                    f.write(':' + str(id))
                with open('data_bl.txt', 'r') as f:
                    text_bl = f.readline()
                open("data_bl.txt", 'w').close()
                return text_bl

            info = self.cur.execute(f'SELECT black_list FROM users WHERE userid={self.id}')
            data_bl0 = BlackL_txt_file_costil(info, user2_id)
            self.cur.execute(f"UPDATE users SET black_list='{data_bl0}' WHERE userid={int(self.id)};")
            info2 = self.cur.execute(f'SELECT black_list FROM users WHERE userid={user2_id}')
            data_bl1 = BlackL_txt_file_costil(info2, self.id)
            self.cur.execute(f"UPDATE users SET black_list='{data_bl1}' WHERE userid={int(user2_id)};")
            self.conn.commit()
            remove('data_bl.txt')
            text_pair = ''
            with open('Pairs.txt', 'r+') as f:
                text_pair = ''.join((line for line in tuple(f.readlines()) if str(self.id) not in line))
            open('Pairs.txt', 'w').close()
            with open('Pairs.txt', 'r+') as f:
                f.write(text_pair)
            self.clear_queue(int(self.id), int(user2_id))
            return (user2_id, self.id)
        else:
            print('We have this id in base')
            return None

    def registration(self):
        # проверка есть ли userid в таблице users
        info = self.cur.execute('SELECT userid FROM users WHERE userid=?', (int(self.id),))
        if info.fetchone() is None:
            # если человека нету в бд
            self.add_into_base(f"INSERT INTO users VALUES({int(self.id)}, 0, ' ', 'None');")
            return "Added"
        else:
            # если человек есть в бд
            return "Been"


conn = sqlite3.connect('BASE.db', check_same_thread=False)
cur = conn.cursor()
local_user = ''


offset = 0 # for added up to date

phrase_dont_show = bad_phrase_in_dialog.phrase


def new_bl():
    info2 = cur.execute(f'SELECT black_list FROM users')
    cur.execute(f"UPDATE users SET black_list=' '")
    conn.commit()

def reply_keyboard(chat_id, data_buttons, text):
    URL = 'https://api.telegram.org/bot'
    TOKEN = setting
    reply_markup ={"keyboard": data_buttons, "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, "text":text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

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

def create_request_audio(chat_id, file_id, parse_mode='HTML'): #sendVideoNote
    URL = 'https://api.telegram.org/bot'
    TOKEN = setting
    message_data = { #create requests for send message
    'chat_id': chat_id,
    'audio': file_id,
    #'reply_to_message_id': update['message']['message_id'], # sendo to reply?? wtf
    'parse_mode': parse_mode # about formate text down
    }
    try:
        request = requests.post(URL+TOKEN+'/sendAudio', data=message_data)
    except:
        print('Error')
        return False
    finally:
        #if not request.status_code == 200:
        #    return 200
        #else:
        print('Succeseful')
        return request

def create_request_video(chat_id, file_id, parse_mode='HTML'): #
    URL = 'https://api.telegram.org/bot'
    TOKEN = setting
    message_data = { #create requests for send message
    'chat_id': chat_id,
    'video_note': file_id,
    #'reply_to_message_id': update['message']['message_id'], # sendo to reply?? wtf
    'parse_mode': parse_mode # about formate text down
    }
    try:
        request = requests.post(URL+TOKEN+'/sendVideoNote', data=message_data)
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
        if line not in ['', ' '] and '=' in line:
            print(line)
            first, second = line[0:len(line)-1].split(';')[0], line[0:len(line)-1].split(';')[1]
            dict_pairs[first.split('=')[0]] = first.split('=')[1]
            dict_pairs[first.split('=')[1]] = first.split('=')[0]
            dict_pairs[second.split('=')[0]] = second.split('=')[1]
            dict_pairs[second.split('=')[1]] = second.split('=')[0]
        #else:
        #    print('bug with pairs fixed')
        #print(line)
    return dict_pairs

def geo_data_place(latitude, longitude):
    token = geo
    headers = {'Accept-Language': "ru"}
    local_user.upd_coord(latitude, longitude)
    local_user.check_coord()
    adress = requests.get(f"https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={latitude}&lon={longitude}&format=json", headers=headers).json()
    return f'Your home {adress.get("display_name")}'

def bot_rules():
    text = "https://telegra.ph/Pravila-anonimnogo-Dimitrovgradskogo-chata-qiwvi-bot-08-29"
    return text

def clear_spam():
    with open("spam.txt", "w") as f:
        f.write('')


def check_update():
    global offset, local_user, users_pair


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
    minutes = int(datetime.now().strftime("%M:%S").split(':')[0])
    hours = int(datetime.now().strftime("%H:%M").split(':')[0])
    sec = int(datetime.now().strftime("%M:%S").split(':')[1])
    if  minutes % 10 == 0 and sec in [i for i in range(0, 10)]: # каждые 10 минут 0-10 секунд
        new_bl()

    if minutes == 54 and hours % 5 == 0 and sec in [i for i in range(0, 10)]:
        clear_spam()

    for update in request.json()['result']:
        try:
            offset = update['update_id'] # подтверждаем обновление


            users_pair = pairs_transform()
            print(update)

            if 'edited_message' not in update:
                local_user = Anonims(update['message']['chat']['id'])

                if (user_location := update['message'].get('location')):
                    # один раз отправлять геоданные
                    geo_data_place(user_location['latitude'], user_location['longitude'])
                    reply_keyboard(update['message']['chat']['id'], [[{"text":"/search - 🔍 Поиск собеседника"}]], "Поиск собеседника в Димитровграде.")

                if 'text' in update['message']:
                    print(str(update['message']['chat']['id']) + ': - ' + update['message']['text'])

                    if '/stop' in update['message']['text']:

                        if local_user.spam_control(): #true - нету в списке
                            create_request(update['message']['chat']['id'], 'Последние <a href="https://t.me/DDqiwvi">новости</a> по боту 👉🏻👉🏻👉🏻')
                        if str(update['message']['chat']['id']) in list(pairs_transform().keys()):
                            users_idss = local_user.stop(users_pair[str(update['message']['chat']['id'])])
                            if users_idss is not None:
                                create_request(str(users_idss[0]), "❌ Связь оборвана")
                                reply_keyboard(str(users_idss[0]), [[{"text":"/info -  ℹ️ Справка по боту"}], [{"text":"/search - 🔍 Поиск собеседника"}]], "Чтобы начать поиск нового собеседник нажмите /search")
                                create_request(str(users_idss[1]), "❌ Связь оборвана")
                                reply_keyboard(str(users_idss[1]), [[{"text":"/info -  ℹ️ Справка по боту"}], [{"text":"/search - 🔍 Поиск собеседника"}]], "Чтобы начать поиск нового собеседник нажмите /search")
                        else:
                            create_request(update['message']['chat']['id'], 'Вы не в диалоге')
                            local_user.clear_solo_queue()
                    if str(update['message']['chat']['id']) in list(users_pair.keys()) and update['message']['text'] not in phrase_dont_show:
                        create_request(int(users_pair[str(update['message']['chat']['id'])]), update['message']['text'])

                    if local_user.checkPairs():

                        if '/search' in update['message']['text']:

                            if local_user.check_coord() == 'None' or  local_user.check_coord() in " ":
                                create_request(update['message']['chat']['id'], "Вы не указали ваше местоположение. Нажмите кнопку 'Где я нахожусь?'")
                                reply_keyboard(update['message']['chat']['id'], [[{"request_location":True, "text":"🌍 Где я нахожусь ?"}]], "Записываем ваше новое местоположение.")
                            elif town in geo_data_place(local_user.check_coord().split('%')[0], local_user.check_coord().split('%')[1]):
                                reply_keyboard(update['message']['chat']['id'], [[{"text":"/info -  ℹ️ Справка по боту"}], [{"text":"/stop - ❌ Конец диалога"}]], "Чтобы остановить поиск напишите - /stop")
                                create_request(update['message']['chat']['id'], "Ищем, дрищем...\nЕсли долго ищет, нажмите повторно /search")
                                local_user.add_queue()
                            else:
                                create_request(update['message']['chat']['id'], "Вы не имеете доступа к анонимному боту.")
                        if  '/start' in update['message']['text']:
                            reg_commit = local_user.registration()
                            if reg_commit == "Added":
                                reply_keyboard(update['message']['chat']['id'], [[{"text":"/info -  ℹ️ Справка по боту"}]], "Новичок, это хорошо!")
                            elif reg_commit == "Been":
                                reply_keyboard(update['message']['chat']['id'], [[{"text":"/info -  ℹ️ Справка по боту"}]], 'Мы вас помним! нажмите /search - 🔍 для поиска собеседника')
                        if  '/info' in update['message']['text']:
                            message = '/info -  ℹ️ Справка по боту\n/start - 🏁 Начать\n/search - 🔍 Поиск собеседника\n/stop - ❌ Конец диалога\n/rules - 👮 правила бота‍'
                            create_request(update['message']['chat']['id'], message)
                            reply_keyboard(update['message']['chat']['id'], [[{"request_location":True, "text":"🌍 Где я нахожусь ?"}], [{"text":"/start - 🏁 Начать"}], [{"text":"/search - 🔍 Поиск собеседника"}], [{"text":"/stop - ❌ Конец диалога"}], [{"text":"/rules - 👮 правила бота"}]], "Проверяем ваше новое местоположение")
                        if '/rules' in update['message']['text']:
                            create_request(update['message']['chat']['id'],  f'<a href="{bot_rules()}">Правила бота</a>')
                            reply_keyboard(update['message']['chat']['id'], [[{"text":"/info -  ℹ️ Справка по боту"}], [{"text":"/search - 🔍 Поиск собеседника"}]], 'Прочтите внимательно!')

                #костыль только для аудио
                if str(update['message']['chat']['id']) in list(users_pair.keys()) and 'voice' in update['message']:
                    print('audio')
                    create_request_audio(int(users_pair[str(update['message']['chat']['id'])]), update['message']['voice']['file_id'])

                if str(update['message']['chat']['id']) in list(users_pair.keys()) and 'video_note' in update['message']:
                    print('video')
                    create_request_video(int(users_pair[str(update['message']['chat']['id'])]), update['message']['video_note']['file_id'])

                answer = tuple(local_user.want_search())
                print(answer)
                if type(answer) == type(("",)) and answer[0] != 'N':
                    with open('Pairs.txt', 'a') as f:
                        rules = local_user.alg_sort(answer) # взвращает словарь
                        keys_black_list = tuple(rules.keys())
                        right_pairs = set()
                        for i in range(len(keys_black_list)):
                            for j in range(i+1, len(keys_black_list)):
                                # основные проверки, что есть в black листе или нету и нету id уже в списке
                                check_first = keys_black_list[j] not in right_pairs
                                check_second = keys_black_list[i] not in right_pairs
                                if str(keys_black_list[i]) not in rules[keys_black_list[j]] and check_first and check_second:

                                    right_pairs.add((keys_black_list[i], keys_black_list[j]))
                                    break
                        for id_1, id_2 in right_pairs:
                            create_request(str(id_1), "✅ Связь установлена")
                            create_request(str(id_2), "✅ Связь установлена")
                            print(id_1, id_2, "LolBol")
                            f.write(str(id_1) + '=' + str(id_2) + ';' + str(id_2) + '=' + str(id_1)+'\n')
                            local_user.clear_queue(id_1, id_2) # пофиксить очищение + идея: можно отправлять фото и видео строго поле 5 сообщения


        except IndexError:
            print("Ignore Error Index out of range in adding in queue from bot", traceback.format_exc())
        except Exception as e:
            print(traceback.format_exc(), 'Bag ignor')



while True:
    try:
        check_update()
    except KeyboardInterrupt: # if I stop bot
        print('bb')
        break
