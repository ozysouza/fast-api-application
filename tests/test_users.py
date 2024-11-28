from app import schemas
from app.config import settings
import jwt
import pytest


def test_login_user(test_first_user, client):
    res = client.post(
        "/login",
        data={
            "username": test_first_user['email'],
            "password": test_first_user['password']
        })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_first_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ('wrongEmail@gmail.com', settings.DATABASE_PASSWORD, 403),
        ('test@gmail.com', 'wrongPassword', 403),
        ('wrongEmail@gmail.com', 'wrongPassword', 403)
    ]
)
def test_incorrect_login(test_first_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        })

    assert res.status_code == status_code
