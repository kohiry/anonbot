import requests
from info import setting


offset = 0 # for added up to date


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
        message_data = { #create requests for send message
        'chat_id': update['message']['chat']['id'],
        'text': "Lol <b>kek</b>",
        'reply_to_message_id': update['message']['message_id'], # sendo to reply?? wtf
        'parse_mode': 'HTML' # about formate text down
        }

        try:
            request = requests.post(URL+TOKEN+'/sendMessage', data=message_data)
        except:
            print('Error')
            return False
        if not request.status_code == 200:
            return 200


while True:
    try:
        check_update()
    except KeyboardInterrupt: # if I stop bot
        print('bb')
        break
