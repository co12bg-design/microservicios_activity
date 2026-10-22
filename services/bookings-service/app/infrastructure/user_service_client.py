from uuid import UUID

import httpx


class UserServiceUnavailableError(Exception):
    """No fue posible consultar users-service."""


class UserServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def exists(self, user_id: UUID) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/users/{user_id}", timeout=2.0)
        except httpx.RequestError as error:
            raise UserServiceUnavailableError from error

        if response.status_code == 404:
            return False
        if response.status_code != 200:
            raise UserServiceUnavailableError(
                f"users-service respondió con HTTP {response.status_code}"
            )
        return True
