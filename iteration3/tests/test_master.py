import time
from fastapi.testclient import TestClient
from app.master import app, HEARTBEATS, get_host_status, not_quorum


client = TestClient(app)


def test_root():
    # check the HEARTBEATS
    assert HEARTBEATS == 3.0

    # get the initial list of messages
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []

    # add the first message
    response = client.post("/", json={"wc": 1, "text": "message 0"})
    assert response.status_code == 200
    assert response.json() == {'ask': 1, 'text': 'message 0', 'id': 0}

    # check the messages in the list
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['message 0']


def test_health():
    # get the initial list of messages
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == list()

    # add the first host
    response = client.post("/health", json={"hostname": "slave_1", "delivered": 0})
    assert response.status_code == 200
    assert response.json() == {'ask': 1, 'hostname': 'slave_1'}

    assert get_host_status('slave_1') == 'Healthy'
    assert not_quorum(1) == False
    assert not_quorum(2) == False
    time.sleep(3)
    assert get_host_status('slave_1') == 'Suspected'
    assert not_quorum(1) == False
    assert not_quorum(2) == False
    time.sleep(3)
    assert get_host_status('slave_1') == 'Unhealthy'
    assert not_quorum(1) == False
    assert not_quorum(2) == True

    # get the list of messages
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == [{'hostname': 'slave_1', 'status': 'Unhealthy'}]

    # add message
    response = client.post("/", json={"wc": 2, "text": "message does not have a quorum"})
    assert response.status_code == 200
    assert response.json() == {'ask': 0, 'text': 'does not have a quorum'}

    # add the first host
    response = client.post("/health", json={"hostname": "slave_1", "delivered": 0})
    assert response.status_code == 200
    assert response.json() == {'ask': 1, 'hostname': 'slave_1'}

    # get the list of messages
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == [{'hostname': 'slave_1', 'status': 'Healthy'}]

