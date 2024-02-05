import requests

BASE_URL = "http://127.0.0.1:8000"

def reset_state():
    response = requests.post(f"{BASE_URL}/reset")
    assert response.status_code == 200

def test_reset_state():
    reset_state()

def test_get_balance_non_existing_account():
    reset_state()
    response = requests.get(f"{BASE_URL}/balance?account_id=1234")
    assert response.status_code == 404

def test_create_account_with_initial_balance():
    reset_state()
    response = requests.post(f"{BASE_URL}/event", json={"type": "deposit", "destination": "100", "amount": 10})
    assert response.status_code == 201
    assert response.json() == {"destination": {"id": "100", "balance": 10}}

def test_deposit_into_existing_account():
    test_create_account_with_initial_balance()
    response = requests.post(f"{BASE_URL}/event", json={"type": "deposit", "destination": "100", "amount": 10})
    assert response.status_code == 201
    assert response.json() == {"destination": {"id": "100", "balance": 20}}

def test_get_balance_existing_account():
    test_deposit_into_existing_account()
    response = requests.get(f"{BASE_URL}/balance?account_id=100")
    assert response.status_code == 200
    assert response.json() == 20

def test_withdraw_from_non_existing_account():
    reset_state()
    response = requests.post(f"{BASE_URL}/event", json={"type": "withdraw", "origin": "200", "amount": 10})
    assert response.status_code == 404

def test_withdraw_from_existing_account():
    test_deposit_into_existing_account()
    response = requests.post(f"{BASE_URL}/event", json={"type": "withdraw", "origin": "100", "amount": 5})
    assert response.status_code == 201
    assert response.json() == {"origin": {"id": "100", "balance": 15}}

def test_transfer_from_existing_account():
    test_deposit_into_existing_account()  
    response = requests.post(f"{BASE_URL}/event", json={"type": "transfer", "origin": "100", "amount": 10, "destination": "300"})
    assert response.status_code == 201
    assert response.json() == {"origin": {"id": "100", "balance": 0}, "destination": {"id": "300", "balance": 10}}

def test_transfer_from_non_existing_account():
    reset_state()
    response = requests.post(f"{BASE_URL}/event", json={"type": "transfer", "origin": "200", "amount": 15, "destination": "300"})
    assert response.status_code == 404
