from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app import models
from tests.utils import randon_string, randon_email
import pytest

from app.main import app
from app.database import get_session
from app.ouath2 import create_access_token
from app.config import settings

POSTGRES_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}_test"


@pytest.fixture(scope="function")
def session():
    engine = create_engine(POSTGRES_DATABASE_URL)
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)


@pytest.fixture()
def test_first_user(client):
    user_data = {
        "email": randon_email(),
        "password": randon_string()
    }

    res = client.post(
        "/users",
        json=user_data
    )

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def test_second_user(client):
    user_data = {
        "email": randon_email(),
        "password": randon_string()
    }

    res = client.post(
        "/users",
        json=user_data
    )

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_first_user):
    return create_access_token({
        "user_id": test_first_user['id']
    })


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_first_user, test_second_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_first_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_first_user['id']
    },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_first_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_second_user['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
