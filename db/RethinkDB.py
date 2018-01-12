import rethinkdb as r


class RethinkDB(object):
    """
    Connecting to RethinkDB.
    """

    # The name of the entity.
    entity = ''

    # A DB object.
    db = {}

    # Holds the connection to DB
    r = {}

    def setSettings(self, entity):
        """
        Constructor.

        :param entity:
            The entity name.
        """
        self.entity = entity

        # todo: get the settings form a json file.
        settings = {'host': 'localhost', 'port': 28015, 'db': 'linkedin'}
        self.connect(settings)

        if not self.tableExists():
            self.createTable()

    def connect(self, settings):
        """
        Set up the connection to the DB.

        :param settings:
            The settings of the DB.

        :return:
        """
        self.r = r.connect(settings['host'], settings['port'])
        self.db = r.db(settings['db'])

    def createTable(self):
        """
        Creating the table of the entity.

        :return:
        """
        return self.db.table_create(self.entity).run(self.r)

    def tableExists(self):
        """
        Checking if a table exists or not.

        :return:
        """
        return self.entity in self.db.table_list().run(self.r)

    def getTable(self):
        """
        Get the table of the entity.

        :return:
        """
        return self.db.table(self.entity)

    def insert(self, object):
        """
        Creating an object.

        :param object:
            The object it self.

        :return:
            The new object.
        """
        results = self.getTable().insert(object).run(self.r)
        object['id'] = results['generated_keys'][0]
        return object

    def load(self, id):
        """
        Loading an object from the DB.

        :param id:
            The ID of the object.

        :return:
            The object from the DB.
        """
        return self.getTable().get(id).run(self.r)

    def update(self, object):
        """
        Updating an object.

        :param object:
            The object to update.

        :return:
        """
        return self.getTable().update(object).run(self.r)

    def delete(self, id):
        """
        Deleting an object.

        :param id:
            The ID of the object.

        :return:
        """
        return self.getTable().filter(r.row["id"] == id).delete().run(self.r)
