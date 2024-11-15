from fastapi.testclient import TestClient
from app.master import app


client = TestClient(app)


def test_get_messages_0():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []

def test_post_messages_1():
    response = client.post("/", json={"wc": 1, "text": "message 0"})
    assert response.status_code == 200
    assert response.json() == {'id': 0, 'text': 'message 0'}

def test_get_messages_1():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['message 0']

# def test_post_messages_2():
#     response = client.post("/", json={"id": 0, "text": "message 0"})
#     assert response.status_code == 200
#     assert response.json() == {'ask': 1, 'item': {'id': 0, 'text': 'message 0'}}

# def test_get_messages_2():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == ['message 0', 'message 1']


# def test_get_sleep_1():
#     response = client.get("/sleep")
#     assert response.status_code == 200
#     assert response.json() ==  {'sleep': {'time': 0}} 

# def test_post_sleep():
#     response = client.post("/sleep", json={"time": 0.99})
#     assert response.status_code == 200
#     assert response.json() ==  {'sleep': {'time': 0.99}} 

# def test_get_sleep_2():
#     response = client.get("/sleep")
#     assert response.status_code == 200
#     assert response.json() ==  {'sleep': {'time': 0.99}} 
