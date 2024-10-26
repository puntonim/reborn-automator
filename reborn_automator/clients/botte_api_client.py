import requests

from ..conf import settings


class BotteApiClient:
    URL = settings.BOTTE_BASE_URL + "/message"
    DEFAULT_HEADERS = {"Authorization": settings.BOTTE_AUTH_TOKEN}

    def send_telegram_message(self, text) -> dict:
        """
        Example:
            $ curl -X POST https://iwjuceybm1.execute-api.eu-south-1.amazonaws.com/message \
               -H 'Authorization: XXX' \
               -d '{"text": "Hello World"}'
               
            {
                "message_id": 22767,
                "from": {
                    "id": 6570886232,
                    "is_bot": true,
                    "first_name": "Botte BOT",
                    "username": "realbottebot",
                },
                "chat": {
                    "id": 2137200685,
                    "first_name": "Paolo",
                    "username": "puntonim",
                    "type": "private",
                },
                "date": 1729936792,
                "text": "Hello World",
            }
        """
        headers = {**self.DEFAULT_HEADERS}
        payload = {"text": text}
        response = requests.post(self.URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
