import botte_lambda_client


class BotteLambdaClient:
    def send_telegram_message(self, text):
        client = botte_lambda_client.BotteLambdaClient()
        response, status_code = client.send_message(text, sender_app="REBORN_AUTOMATOR")
        return response, status_code
