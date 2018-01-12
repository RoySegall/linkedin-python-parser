from apistar import Route

from endpoints.BaseRoute import BaseRoute


class SearchRoute(BaseRoute):
    """
    This is the route for searching for previous scraped profiles.
    """

    def Routes(self):
        return [
            Route('/', 'GET', self.searchGet),
            Route('/', 'POST', self.searchPost),
            Route('/', 'PATCH', self.searchPatch),
            Route('/', 'DELETE', self.searchDelete),
        ]

    def searchGet(self):
        return {}

    def searchPost(self):
        return {}

    def searchPatch(self):
        return {}

    def searchDelete(self):
        return {}
