import pytest
from httpx import AsyncClient

from tests import utils


@pytest.mark.parametrize(
    "send_token, right_status_code, is_admin",
    [
        (True, 200, True),
        (True, 200, False),
        (False, 401, True)
    ]
)
async def test_get_current_user(ac: AsyncClient, send_token: bool, right_status_code: int, is_admin: bool):
    email = "test-get-current-user@mail.ru"
    password = "123"
    response_create = await ac.post(
        url="/api/v1/auth/create_user",
        json={
            "email": email,
            "name": "string",
            "lastname": "string",
            "patronymic": "string",
            "is_admin": is_admin,
            "password": password
        }
    )
    id = response_create.json().get("id")

    response_login = await ac.post(
        url="/api/v1/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": email,
            "password": password,
            "grant_type": "password"
        }
    )
    access_token = response_login.json().get("access_token")
    if send_token:
        response = await ac.get(
            url="/api/v1/auth/profile/my",
            headers={"authorization": f"Bearer {access_token}"}
        )
    else:
        response = await ac.get(
            url="/api/v1/auth/profile/my",
        )
    assert response.status_code == right_status_code
    await utils.delete_user(email)
