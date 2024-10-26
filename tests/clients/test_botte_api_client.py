from reborn_automator.clients.botte_api_client import BotteApiClient


class TestBotteApiClient:
    def test_happy_flow(self):
        response = BotteApiClient().send_telegram_message("Hello World")
        assert response
