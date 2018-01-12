import rethinkdb as r


class RethinkDB(object):
    """
    Connecting to RethinkDB.
    """

    # The name of the entity.
    entity = ''

    # A DB object.
    db = {}

    def __init__(self, entity):
        """
        Constructor.

        :param entity:
            The entity name.
        """
        self.entity = entity

        # todo: get the settings form a json file.
        settings = {'host': 'localhost', 'port': 28015, 'db': 'linkedin'}
        self.connect(settings)

    def connect(self, settings):
        self.r = r.connect(settings['host'], settings['port'])
        self.db = r.db(settings['db'])

    def createTable(self):
        self.db.table_create(self.entity).run(self.r)

    def insert(self, object):
        """
        Creating an object.

        :param object:
            The object it self.

        :return:
            The new object.
        """
        self.db.table(self.entity).insert(object).run(self.r)

    def load(self, id):
        """
        Loading an object from the DB.

        :param id:
            The ID of the object.

        :return:
            The object from the DB.
        """
        return {}

    def update(self, object):
        """
        Updating an object.

        :param object:
            The object to update.

        :return:
        """
        return {}

    def delete(self, id):
        """
        Deleting an object.

        :param id:
            The ID of the object.

        :return:
        """
        return {}
