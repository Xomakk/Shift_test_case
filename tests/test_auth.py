import pytest
from httpx import AsyncClient

from src.auth import models
from tests.conftest import delete_user


class Token(object):
    instance = None
    access_token: str = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Token, cls).__new__(cls)
        return cls.instance


@pytest.mark.parametrize(
    "email, right_status_code, password, right_response_content",
    [
        (
                "test@mail.ru",
                200,
                "123",
                b'{"email":"test@mail.ru","name":"string","lastname":"string","surname":"string","id":1}'
        ),
        (
                "test",
                422,
                "123",
                b'{"detail":[{"loc":["body","email"],"msg":"value is not a'
                b' valid email address","type":"value_error.email"}]}'
        ),
        (
                "test@mail.ru",
                422,
                None,
                b'{"detail":[{"loc":["body","password"],"msg":"none is not an allowed value","'
                b'type":"type_error.none.not_allowed"}]}'
        ),
    ]
)
async def test_create_user(
        ac: AsyncClient,
        email: str,
        right_status_code: int,
        password: str,
        right_response_content: str
):
    response = await ac.post(
        url="/api/auth/create_user",
        json={
            "email": email,
            "name": "string",
            "lastname": "string",
            "surname": "string",
            "password": password
        }
    )
    assert response.status_code == right_status_code
    assert response.content == right_response_content
    await delete_user(email)


@pytest.mark.parametrize(
    "username, password, right_status_code",
    [
        ("test-login@mail.ru", "123", 200),
        ("test-login@mail.ru", "12345", 400),
        ("test123@mail.ru", "123", 400),
    ]
)
async def test_login_user(ac: AsyncClient, username: str, password: str, right_status_code: int):
    await ac.post(
        url="/api/auth/create_user",
        json={
            "email": "test-login@mail.ru",
            "name": "string",
            "lastname": "string",
            "surname": "string",
            "password": "123"
        }
    )

    response = await ac.post(
        url="/api/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": username,
            "password": password,
            "grant_type": "password"
        }
    )
    assert response.status_code == right_status_code
    await delete_user(username)


@pytest.mark.parametrize(
    "send_token, right_status_code",
    [
        (True, 200),
        (False, 401)
    ]
)
async def test_get_current_user(ac: AsyncClient, send_token: bool, right_status_code: int):
    email = "test-get-current-user@mail.ru"
    password = "123"
    await ac.post(
        url="/api/auth/create_user",
        json={
            "email": email,
            "name": "string",
            "lastname": "string",
            "surname": "string",
            "password": password
        }
    )

    response = await ac.post(
        url="/api/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": email,
            "password": password,
            "grant_type": "password"
        }
    )
    token = response.json().get("access_token")
    if send_token:
        response = await ac.get(
            url="/api/auth/user",
            headers={"authorization": f"Bearer {token}"}
        )
    else:
        response = await ac.get(
            url="/api/auth/user",
        )
    assert response.status_code == right_status_code
    await delete_user(email)


@pytest.mark.parametrize(
    "send_token, right_status_code",
    [
        (True, 200),
        (False, 401)
    ]
)
async def test_logout(ac: AsyncClient, send_token: bool, right_status_code: int):
    email = "test-logout@mail.ru"
    password = "123"
    await ac.post(
        url="/api/auth/create_user",
        json={
            "email": email,
            "name": "string",
            "lastname": "string",
            "surname": "string",
            "password": password
        }
    )

    response = await ac.post(
        url="/api/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": email,
            "password": password,
            "grant_type": "password"
        }
    )
    token = response.json().get("access_token")
    if send_token:
        response = await ac.get(
            url="/api/auth/logout",
            headers={"authorization": f"Bearer {token}"}
        )
    else:
        response = await ac.get(
            url="/api/auth/logout"
        )
    assert response.status_code == right_status_code
    await delete_user(email)
