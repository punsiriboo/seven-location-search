import json
import requests
from system import Configurator


class Requester:

    def __init__(self, config: Configurator):
        self.configurator = config
    
    def post_dialogflow(self, request):
        url = self.configurator.get('dialogflow.webhook')
        headers = dict()
        for key,value in request.headers.items():
            headers[key] = value
        headers['Host'] = self.configurator.get('dialogflow.host')
        response = requests.post(url, data = json.dumps(request.json), headers=headers)
    
    def post_store_search(self, event):
        user_id = event.source.user_id
        url = self.configurator.get('api.location.store')
        headers = { 'Content-Type': 'application/json'}
        payload = {
            'replyToken': event.reply_token,
            'source': { 'type': 'user', 'userId': user_id },
            'postback': { 'data': event.postback.data},
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response
