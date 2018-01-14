from apistar import Response


class BaseRoute(object):
    """
    Base class for routes.
    """

    # The response code for the current request.
    response_code = 200

    # List of headers.
    headers = {}

    # Set the body the request.
    body = {}

    def Routes(self):
        """
        Defining the actions for the current route.

        :return:
            List of routes.
        """
        pass
