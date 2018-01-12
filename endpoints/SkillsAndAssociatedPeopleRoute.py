from apistar import Route

from endpoints.BaseRoute import BaseRoute


class SkillsAndAssociatedPeopleRoute(BaseRoute):
    """
    This is the route for searching skills and associated people.
    """

    def Routes(self):
        return [
            Route('/', 'GET', self.skillsGet),
            Route('/', 'POST', self.skillsPost),
            Route('/', 'PATCH', self.skillsPatch),
            Route('/', 'DELETE', self.skillsDelete),
        ]

    def skillsGet(self):
        return {}

    def skillsPost(self):
        return {}

    def skillsPatch(self):
        return {}

    def skillsDelete(self):
        return {}
