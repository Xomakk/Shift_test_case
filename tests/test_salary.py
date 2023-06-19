import pytest
from httpx import AsyncClient

from tests.conftest import delete_user


@pytest.mark.parametrize(
    "send_token, right_status_code, size, increase_date",
    [
        (True, 200, 100, "2023-11-19T09:33:55.844"),
        (True, 422, 15.6, "2023-45-19T09:33:55.844"),
        (True, 200, 15.6, "2023-06-19T10:25:17.468"),
        (True, 200, "123", "2023-06-19T10:25:17.468"),
        (True, 400, "123", "2023-06-19T10:25:17.468Z"),
        (False, 401, 100, "2023-11-19T09:33:55.844")
    ]
)
async def test_edit_salary(ac: AsyncClient, send_token: bool, right_status_code: int, size: int, increase_date: str):
    email = "test-edit-salary@mail.ru"
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
        response = await ac.post(
            url="/api/salary/edit",
            headers={"authorization": f"Bearer {token}"},
            json={
              "size": size,
              "increase_date": increase_date
            }
        )
    else:
        response = await ac.post(
            url="/api/salary/edit",
            json={
                "size": size,
                "increase_date": increase_date
            }
        )
    assert response.status_code == right_status_code
    await delete_user(email)


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
            url="/api/salary/my",
            headers={"authorization": f"Bearer {token}"},
        )
    else:
        response = await ac.get(
            url="/api/salary/my",
        )
    assert response.status_code == right_status_code
    await delete_user(email)
