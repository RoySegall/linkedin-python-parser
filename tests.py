import json
import pdb

from apistar.test import TestClient
from app import app
from models.Profile import Profile


def test_skills_searching():
    """
    Testing the search by skills.
    """
    profile = Profile()

    # First clean any data from the DB.
    if profile.tableExists():
        profile.deleteTable()
        profile.createTable()

    # Create dummy entries.
    profile.insert(json.load(open('dummy_json/roy.json')))
    profile.insert(json.load(open('dummy_json/david.json')))
    profile.insert(json.load(open('dummy_json/nir.json')))

    # Start to run tests against the API. First, get the application.
    client = TestClient(app)

    # Search by skills.
    json_response = client.post('/search-by-skills', json={'skill': 'Drupal'})

    assert json_response.json()[0]['match'] == 11

    # Search for JavaScript.
    json_response = client.post('/search-by-skills', json={'skill': 'JavaScript'})
    matches = {
        'nirgn': 18,
        'roy-segall-304b054a': 16,
        'davidbronfen': 12
    }

    for profile in json_response.json():
        assert profile["match"] == matches[profile['user_id']]


def test_search_by_name():
    """
    Searching by the name.
    :return:
    """

    # Start to run tests against the API. First, get the application.
    client = TestClient(app)
    response = client.post('/search-by-name', json={'name': 'Roy'})
    json_response = response.json()

    # Basic search.
    assert json_response[0]['current_position'] == 'gizra'
    assert json_response[0]['current_title'] == 'Team leader at Gizra'
    assert json_response[0]['name'] == 'Roy Segall'

    response = client.post('/search-by-name', json={'name': 'David'})
    json_response = response.json()

    # Basic search.
    assert json_response[0]['current_position'] == 'Netcraft Israel'
    assert json_response[0]['current_title'] == 'Frontend Developer at Netcraft Israel'
    assert json_response[0]['name'] == 'David Bronfen'
