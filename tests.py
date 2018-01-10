from apistar.test import TestClient
from app import app, upload


def test_welcome():
    """
    Testing a view directly.
    """
    data = upload()
    assert data == {'message': 'Not supported for now but will be :).'}


def test_http_request():
    """
    Testing a view, using the test client.
    """
    client = TestClient(app)
    response = client.get('http://localhost/upload')
    assert response.status_code == 405

    response = client.post('http://localhost/upload')
    assert response.status_code == 200
    assert response.json() == {'message': 'Not supported for now but will be :).'}
