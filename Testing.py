from models.Dummy import Dummy
import json
from endpoints.ScrapeRoute import ScrapeRoute


class Testing(object):

    def test_rethinkdb(self):
        """
        Testing insert and load.

        :return:
        """
        # Creating the object.
        dummy = Dummy()

        # Creating the table.
        if not dummy.tableExists():
            dummy.createTable()

        # Insert an obejct to the DB.
        pizza = dummy.insert({'food': 'pizza'})

        # Making sure the object has an ID.
        assert pizza['id'] is not None

        # Loading it from the DB.
        loaded_dummy = dummy.getTable().get(pizza['id'])

        assert loaded_dummy['food'] == pizza['fdood']

    def test_base_scrape(self):
        """
        Testing the base scrape class. We not testing against selenium since setting in on Travis CI will be hell.
        We only test the api functionality.

        :return:
        """
        # Init the object and load the json file.
        route = ScrapeRoute()
        profile = json.load(open('dummy_json/roy.json'))

        # Loading the object one time the the DB.
        results = route.process_results(profile)

        # Extract the ID.
        id = results['id']

        # Asserting some elements.
        assert results['name'] == 'Roy Segall'
        assert results['current_title'] == 'Team leader at Gizra'

        # Change a property and making sure the DB object was updated.
        new_profile = profile
        new_profile['name'] = 'Roy Segall Updated'
        updated_profile = route.process_results(new_profile)

        assert updated_profile['id'] == id
        assert updated_profile['name'] == 'Roy Segall Updated'
