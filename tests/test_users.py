from app import schemas
from app.config import settings
import pytest
from jose import jwt


# def test_root(client, session):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "Hello world - from CNEMRI with love"}
#     assert response.headers["Content-Type"] == "application/json"


def test_create_user(client, session):
    data = {"email": "chouchou@gmail.com", "password": "password123"}
    response = client.post("/users/", json=data)
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "chouchou@gmail.com"


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


@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('cnemri@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('cnemri@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    login_data = dict(
        username=email, password=password)
    response = client.post("/login", data=login_data)
    assert response.status_code == status_code