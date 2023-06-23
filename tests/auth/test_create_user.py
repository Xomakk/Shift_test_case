import pytest
from httpx import AsyncClient

from tests import utils


@pytest.mark.parametrize(
    "username, right_status_code, password",
    [
        (
                "test@mail.ru",
                200,
                "123"
        ),
        (
                "test",
                422,
                "123"
        ),
        (
                "test@mail.ru",
                422,
                None
        ),
    ]
)
async def test_create_user(
        ac: AsyncClient,
        username: str,
        right_status_code: int,
        password: str,
):
    response = await ac.post(
        url="/api/v1/auth/create_user",
        json={
            "email": username,
            "name": "string",
            "lastname": "string",
            "patronymic": "string",
            "is_admin": False,
            "password": password
        }
    )
    assert response.status_code == right_status_code
    await utils.delete_user(username)