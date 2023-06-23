import pytest
from httpx import AsyncClient

from tests import utils


@pytest.mark.parametrize(
    "send_token, right_status_code, is_admin, email",
    [
        (True, 200, True, "test-edit-user-by-id1@mail.ru"),
        (True, 403, False, "test-edit-user-by-id2@mail.ru"),
        (False, 401, True, "test-edit-user-by-id3@mail.ru")
    ]
)
async def test_edit_user_by_id(ac: AsyncClient, send_token: bool, right_status_code: int, is_admin: bool, email: str):
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
        response = await ac.put(
            url=f"/api/v1/auth/profile/edit",
            headers={"authorization": f"Bearer {access_token}"},
            json={
                "id": id,
                "name": "string",
                "lastname": "string",
                "patronymic": "string"
            }
        )
    else:
        response = await ac.put(
            url=f"/api/v1/auth/profile/edit",
        )
    assert response.status_code == right_status_code
    await utils.delete_user(email)
