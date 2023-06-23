import pytest
from httpx import AsyncClient

from tests import utils


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
        url="/api/v1/auth/create_user",
        json={
            "email": "test-login@mail.ru",
            "name": "string",
            "lastname": "string",
            "patronymic": "string",
            "password": "123"
        }
    )

    response = await ac.post(
        url="/api/v1/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": username,
            "password": password,
            "grant_type": "password"
        }
    )
    assert response.status_code == right_status_code
    await utils.delete_user(username)
