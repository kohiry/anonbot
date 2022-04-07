from random import choice


class Anonims:
    def __init__(self, data, id):
        sef.all_user = data # all id
        self.good_data = [] # id status True

    def find_good(self): # True - wanna talk in condition - seeker, false - did't want
        self.good_data = [i for i in self.all_user if i.status == True] # find free users

    def find_pair(self, id):
        while True:
            self.find_good()
            if len(self.good_data) != 0:
                self.friend_id = choice(self.good_data)
                break


class User:
    def __init__(self, id, status=False):
        self.status = status # True/False
        self.id = id
        self.friend_id = 0

    def change_status(self, status):
        self.status = status
