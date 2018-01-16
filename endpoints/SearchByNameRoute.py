import json

from apistar import Route, http, Response
from rethinkdb import r

from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile


class SearchByNameRoute(BaseRoute):
    """
    This is the route for searching for previous scraped profiles.
    """

    def Routes(self):
        return [
            Route('', 'POST', self.search),
        ]

    def search(self, body: http.Body):
        """
        Searching for a user in the DB.

        :return:
        """
        payload = json.loads(body.decode())

        if payload['name'] is None:
            return Response({'message': 'The name property is empty'}, status=401)

        # Get the search text.
        text = payload['name']

        # Init the query operation.
        profile = Profile()
        profiles = profile \
            .getTable() \
            .filter(
                lambda document:
                    document['name'].match(text)
                    | document['current_position'].match(text)
                    | document['current_title'].match(text)
                    | document['summary'].match(text)
            ) \
            .run(profile.r)

        # Search in the text in the name, title, position, summary.
        results = []

        for profile in profiles:
            results.append(profile)

        return results
