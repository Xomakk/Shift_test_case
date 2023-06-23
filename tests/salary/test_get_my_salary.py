import pytest
from httpx import AsyncClient

from tests.utils import delete_user


@pytest.mark.parametrize(
    "send_token, right_status_code",
    [
        (True, 200),
        (False, 401),
    ]
)
async def test_get_my_salary(ac: AsyncClient, send_token: bool, right_status_code: int):
    email = "test-get-salary@mail.ru"
    password = "123"
    response_create = await ac.post(
        url="/api/v1/auth/create_user",
        json={
            "email": email,
            "name": "string",
            "lastname": "string",
            "patronymic": "string",
            "is_admin": False,
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
            url="/api/v1/salary/my",
            headers={"authorization": f"Bearer {access_token}"},
        )
    else:
        response = await ac.get(
            url="/api/v1/salary/my",
        )
    assert response.status_code == right_status_code
    await delete_user(email)
