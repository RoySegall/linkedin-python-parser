from apistar.test import TestClient
from app import app
from models.Profile import Profile


def test_http_request():
    """
    Testing a view, using the test client.
    """
    profile = Profile()

    # First clean any data from the DB.
    profile.deleteTable()

    # Create three elements.

    # Start to run tests against the API.

    assert 1 == 1
