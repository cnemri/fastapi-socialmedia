from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, response.json())
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get('/posts/111')
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize('title, content, published', [
    ('test title', 'test content', True),
    ('test title 2', 'test content 2', False),
    ('test title 3', 'test content 3', True),
])
def test_create_post(authorized_client, test_user, title, content, published, test_posts):
    response = authorized_client.post(
        '/posts/', json=dict(title=title, content=content, published=published))

    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['content'] == content
    assert response.json()['published'] == published
    assert response.json()['owner_id'] == test_user['id']


def test_create_post_default_published(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        '/posts/', json=dict(title='test title', content='test content'))

    assert response.status_code == 201
    assert response.json()['published'] == True


def test_unauthorized_user_create_post(client, test_user):
    response = client.post(
        '/posts/', json=dict(title='test title', content='test content'))
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    # get all posts
    posts = authorized_client.get('/posts/').json()
    assert response.status_code == 204
    assert len(posts) == len(test_posts) - 1


def delete_post_not_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete('/posts/111')
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'owner_id': test_user['id']
    }
    response = authorized_client.put(
        f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 200
    assert response.json()['title'] == data['title']
    assert response.json()['content'] == data['content']
    assert response.json()['owner_id'] == test_user['id']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'owner_id': test_user['id']
    }
    response = authorized_client.put(
        f'/posts/{test_posts[3].id}', json=data)
    assert response.status_code == 403


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'owner_id': test_user['id']
    }
    response = authorized_client.put(
        f'/posts/111', json=data)
    assert response.status_code == 404