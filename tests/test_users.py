from app import schemas
from app.config import settings
from .database import client, session
import pytest
from jose import jwt


# def test_root(client, session):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "Hello world - from CNEMRI with love"}
#     assert response.headers["Content-Type"] == "application/json"

@pytest.fixture
def test_user(client):
    # user_data json constituted of email and password fields
    user_data = {
        "email": "charara@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


def test_create_user(client, session):
    data = {"email": "chararo@gmail.com", "password": "password123"}
    response = client.post("/users/", json=data)
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "chararo@gmail.com"


def test_login(client, test_user):
    login_data = dict(
        username=test_user['email'], password=test_user['password'])
    response = client.post("/login", data=login_data)
    login_response = schemas.Token(**response.json())
    # decode jwt token, specify secret key and algorithm
    decoded = jwt.decode(login_response.access_token,
                         settings.secret_key, algorithms=settings.algorithm)
    id = decoded.get('user_id')
    assert id == test_user['id']
    assert response.status_code == 200
