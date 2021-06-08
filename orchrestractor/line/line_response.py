import json, requests


class LineResponse:

    def __init__(self, access_token: str):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def push(self, data): 
        url = 'https://api.line.me/v2/bot/message/push'
        response = requests.post(url, data = data, headers=self.headers)
