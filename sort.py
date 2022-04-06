
class Anonims:
    def __init__(self, data):
        sef.all_user = data # all id
        self.good_data = [] # id status True

    def find_good(self):
        self.good_data = [i for i in self.all_user if i.status == True] # find free users


class User:
    def __init__(self, id, status=False):
        self.status = status # True/False
        self.id = id

    def change_status(self, status):
        self.status = status
