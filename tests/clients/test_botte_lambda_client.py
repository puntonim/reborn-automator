from reborn_automator.clients.botte_lambda_client import BotteLambdaClient


class TestBotteLambdaClient:
    def test_happy_flow(self):
        client = BotteLambdaClient()
        text = "Hello from reborn-automator pytests!"
        response, status_code = client.send_telegram_message(text)
        assert response["text"] == text
        assert status_code == 200
