import pytest

from reborn_automator.clients.reborn_api_client import AuthError, RebornApiClient
from reborn_automator.conf import settings


class TestRebornApiClientLogin:
    def test_happy_flow(self):
        client = RebornApiClient()
        client.login(settings.REBORN_CREDS_USERNAME, settings.REBORN_CREDS_PASSWORD)
        assert client.session_id

    def test_wrong_username(self):
        client = RebornApiClient()
        with pytest.raises(AuthError):
            client.login(
                settings.REBORN_CREDS_USERNAME + "XXX", settings.REBORN_CREDS_PASSWORD
            )

    def test_wrong_password(self):
        client = RebornApiClient()
        with pytest.raises(AuthError):
            client.login(
                settings.REBORN_CREDS_USERNAME, settings.REBORN_CREDS_PASSWORD + "XXX"
            )


class TestRebornApiClientGetPalinsesto:
    def setup_method(self):
        self.client = RebornApiClient()
        self.client.login(
            settings.REBORN_CREDS_USERNAME, settings.REBORN_CREDS_PASSWORD
        )

    def test_happy_flow(self):
        palinsesto = self.client.get_palinsesto()
        assert palinsesto


class TestRebornApiClientBookClass:
    def setup_method(self):
        self.client = RebornApiClient()
        self.client.login(
            settings.REBORN_CREDS_USERNAME, settings.REBORN_CREDS_PASSWORD
        )

    def test_too_early(self):
        response = self.client.book_class(756422, "2024-10-30")
        assert response

    def test_class_id_does_not_exist(self):
        response = self.client.book_class(99, "2024-10-30")
        assert response
