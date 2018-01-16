from db.RethinkDB import RethinkDB


class Profile(RethinkDB):

    def __init__(self):
        super().setSettings('profiles')
