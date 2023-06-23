import pytest
from httpx import AsyncClient

from tests.utils import delete_user


@pytest.mark.parametrize(
    "send_token, right_status_code, email, is_admin",
    [
        (True, 200, "test-get-salary_by_id1@mail.ru", True),
        (True, 403, "test-get-salary_by_id2@mail.ru", False),
        (False, 401, "test-get-salary_by_id3@mail.ru", False),
    ]
)
async def test_get_salary_by_user_id(ac: AsyncClient, send_token: bool, right_status_code: int, email: str,
                                     is_admin: bool):
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
            url=f"/api/v1/salary/get?user_id={id}",
            headers={"authorization": f"Bearer {access_token}"},
        )
    else:
        response = await ac.get(
            url=f"/api/v1/salary/get?user_id={id}",
        )
    assert response.status_code == right_status_code
    await delete_user(email)
