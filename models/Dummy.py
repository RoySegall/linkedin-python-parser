from db.RethinkDB import RethinkDB


class Dummy(RethinkDB):

    def __init__(self):
        super().setSettings('dummy')
