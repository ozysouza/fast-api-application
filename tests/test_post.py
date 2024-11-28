from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostVoteOut(**post)

    posts_map = map(validate, res.json())
    post_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_specific_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/888")
    assert res.status_code == 404
    assert res.json().get('detail') == "Post with ID: 888 was not found!"


def test_get_valid_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVoteOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ('One Piece', 'Rubber Pirate', True),
        ('The History of a Dog', 'Lovely idea', False),
        ('The Sea', 'Interesting approach', True),
    ]
)
def test_create_post(authorized_client, test_first_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published
        }
    )

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_first_user['id']


def test_create_post_default_published_true(authorized_client, test_first_user):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": "The Fantastic Train",
            "content": "History about trains"
        }
    )

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "The Fantastic Train"
    assert created_post.content == "History about trains"
    assert created_post.published == True
    assert created_post.owner.id == test_first_user['id']


def test_unauthorized_user_create_post(client, test_first_user):
    res = client.post(
        "/posts/",
        json={
            "title": "The Fantastic Train",
            "content": "History about trains"
        }
    )
    assert res.status_code == 401
    assert res.json().get('detail') == "Not authenticated"


def test_unauthorized_user_delete_post(client, test_first_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 401
    assert res.json().get('detail') == "Not authenticated"


def test_user_delete_post_wrong_id(authorized_client, test_first_user):
    res = authorized_client.delete(
        "/posts/123123"
    )
    assert res.status_code == 404
    assert res.json().get('detail') == "Post with ID: 123123, does not exist!"


def test_user_delete_post_success(authorized_client, test_first_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 204


def test_user_delete_post_failure_not_owner(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}"
    )
    assert res.status_code == 403
    assert res.json().get('detail') == "Not authorized to perform requested action"


def test_user_update_post(authorized_client, test_first_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=data
    )
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_user_put_post_wrong_id(authorized_client, test_first_user):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": "123123"
    }

    res = authorized_client.put(
        "/posts/123123",
        json=data
    )
    assert res.status_code == 404
    assert res.json().get('detail') == "Post with ID: 123123, does not exist!"


def test_user_update_failure_not_owner(authorized_client, test_first_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json=data
    )

    assert res.status_code == 403
    assert res.json().get('detail') == "Not authorized to perform requested action"


def test_unauthorized_user_put_post(client, test_first_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 401
    assert res.json().get('detail') == "Not authenticated"
