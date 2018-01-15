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
        print(payload['text'])

        if payload['text'] is None:
            return Response({'message': 'The text property it empty'}, status=401)

        # Get the search text.

        # r.db("linkedin").table('profile').filter(function(profile)
        # {
        # return profile("skills").contains(function(skill)
        # {
        # return skill("skill").eq("Go")
        # })
        # })

        profile = Profile()

        cursor = profile \
            .getTable() \
            .filter(lambda profile:
                    profile["skills"].contains(lambda skills: skills['skill'].eq(payload['text']))) \
            .run(profile.r)

        # Search in the text in the name, title, position, summary.

        score = self.calculate_score("", {})

        return list(cursor)

    def calculate_score(self, text, user_object):
        """
        Calculating the score for a user name.

        If the text exists only in the title or the position current position - the score is 1.

        If the text appears in the description of the user and the skills that's mean the user is matching for search
        based on a tech. In that case the person is a good match and the score will be the number or endorsements.

        :param text:
            The text the user searched for.
        :param user_object:
            The user object.

        :return:
            A score based on the object.
        """
        return 1
