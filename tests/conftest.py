from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/fastapi_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    # user_data json constituted of email and password fields
    user_data = {
        "email": "cnemri@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    # user_data json constituted of email and password fields
    user_data = {
        "email": "cha3bolla@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers['Authorization'] = f'Bearer {token}'
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "Test post 1",
            "content": "Test post 1 body",
            "owner_id": test_user['id']
        }, {
            "title": "Test post 2",
            "content": "Test post 2 body",
            "owner_id": test_user['id']
        }, {
            "title": "Test post 3",
            "content": "Test post 3 body",
            "owner_id": test_user['id']
        }, {
            "title": "Test post 4",
            "content": "Test post 4 body",
            "owner_id": test_user2['id']
        }]

    def create_post_model(post_data):
        return models.Post(**post_data)

    new_posts = list(map(create_post_model, post_data))
    session.add_all(new_posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()