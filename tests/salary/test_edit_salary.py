import pytest
from httpx import AsyncClient

from tests.utils import delete_user


@pytest.mark.parametrize(
    "send_token, right_status_code, size, increase_date, is_admin, email",
    [
        (True, 200, 100, "2023-11-19T09:33:55.844", True, "test-edit-salary1@mail.ru"),
        (True, 403, 100, "2023-11-19T09:33:55.844", False, "test-edit-salary2@mail.ru"),
        (True, 422, 15.6, "2023-45-19T09:33:55.844", True, "test-edit-salary3@mail.ru"),
        (True, 200, 15.6, "2023-06-19T10:25:17.468", True, "test-edit-salary4@mail.ru"),
        (True, 200, "123", "2023-06-19T10:25:17.468", True, "test-edit-salary5@mail.ru"),
        (True, 200, "123", "2023-06-19T10:25:17.468Z", True, "test-edit-salary6@mail.ru"),
        (False, 401, 100, "2023-11-19T09:33:55.844", False, "test-edit-salary7@mail.ru")
    ]
)
async def test_edit_salary(ac: AsyncClient, send_token: bool, right_status_code: int, size: int, increase_date: str,
                           is_admin: bool, email: str):
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
            url="/api/v1/salary/edit",
            headers={"authorization": f"Bearer {access_token}"},
            json={
                "size": size,
                "increase_date": increase_date,
                "user_id": id
            }
        )
    else:
        response = await ac.put(
            url="/api/v1/salary/edit",
            json={
                "size": size,
                "increase_date": increase_date,
                "user_id": id
            }
        )
    assert response.status_code == right_status_code
    await delete_user(email)
