import pytest
from app import models


@pytest.fixture()
def test_vote(test_posts, session, test_first_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_first_user['id'])
    session.add(new_vote)
    session.commit()


def test_user_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": test_posts[3].id,
            "dir": 1
        }
    )
    assert res.status_code == 201
    assert res.json().get('message') == "Vote successfully added"


def test_user_cannot_vote_twice_on_same_post(authorized_client, test_first_user, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": test_posts[3].id,
            "dir": 1
        }
    )
    assert res.status_code == 409
    assert res.json().get('detail') == f"User {test_first_user['id']} has already voted on post {test_posts[3].id}"


def test_user_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": test_posts[3].id,
            "dir": 0
        }
    )
    assert res.status_code == 201
    assert res.json().get('message') == "Vote successfully deleted"


def test_user_remove_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": test_posts[3].id,
            "dir": 0
        }
    )
    assert res.status_code == 404
    assert res.json().get('detail') == "Vote does not exist."


def test_user_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": "123131",
            "dir": 0
        }
    )
    assert res.status_code == 404
    assert res.json().get('detail') == "Post with id: 123131 does not exist."


def test_user_vote_unauthorized(client, test_posts):
    res = client.post(
        "/vote/",
        json={
            "post_id": test_posts[1].id,
            "dir": 0
        }
    )
    assert res.status_code == 401
    assert res.json().get('detail') == "Not authenticated"
