import json

from apistar import Route, http, Response
from rethinkdb import r

from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile


class SearchRoute(BaseRoute):
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

        if payload['text'] is None:
            return Response({'message': 'The text property it empty'}, status=401)

        # Get the search text.
        text = payload['text']

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
                    | document['skills'].contains(lambda skills: skills['skill'].match(text))
            ) \
            .run(profile.r)

        # Search in the text in the name, title, position, summary.
        results = []

        for profile in profiles:
            profile['match'] = self.calculate_score(text, profile)
            results.append(profile)

        return results

    def calculate_score(self, text, user_object):
        """
        Calculating the score for a user name.

        Get the rank from the list of fields. Combine it with the amount of times the text appears in the experience
        field. If the user has any educations - add the number of elements.

        :param text:
            The text the user searched for.
        :param user_object:
            The user object.

        :return:
            A score based on the object.
        """
        # Get the rank.
        skill_rank = 0

        for skill in user_object['skills']:
            if text in skill['skill']:
                skill_rank = skill['rank']
                # We found the skill. Break the loop.
                break

        # Get the amount of time from the experience.
        appearing = 0
        for experience in user_object['experience']:
            if text in experience['description']:
                appearing = appearing + 1

        return int(skill_rank) + int(appearing) + len(user_object['education'])
