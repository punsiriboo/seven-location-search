from linebot import (LineBotApi, WebhookParser)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, StickerSendMessage)
from system import Configurator
from api_requester import Requester
from line import LineResponse
import json

configurator = Configurator("private/config.json")
service_requester = Requester(configurator)
line_bot_api = LineBotApi(configurator.get('line.access_token'))
line_response = LineResponse(configurator.get('line.access_token'))
parser = WebhookParser(configurator.get('line.channel_secret'))

def handle_message(request):
    body = request.get_data(as_text=True)
    print("Request: " + body)
    signature = request.headers['X-Line-Signature']
    events = parser.parse(body, signature)
    for event in events:
        user_id=event.source.user_id
        reply_token = event.reply_token
        if event.type == "message":
            if event.message.type == "text":
                service_requester.post_dialogflow(request)
            if event.message.type == "location": 
                latitude = event.message.latitude
                longitude = event.message.longitude 
                with open('message/template_ask_product_type.json') as f: 
                    msg_text = f.read().replace("<:user_id>",user_id).replace("<:latitude>",str(latitude)).replace("<:longitude>",str(longitude))
                line_response.push(json.dumps(json.loads(msg_text)))
            if event.message.type == "audio": 
                line_bot_api.reply_message(reply_token, TextSendMessage(text="you send auido."))
            if event.message.type == "image":  
                line_bot_api.reply_message(reply_token, TextSendMessage(text="you send image."))
            if event.message.type == "sticker":
                package_id = 11539
                sticker_id = 52114112
                line_bot_api.reply_message(reply_token, StickerSendMessage(package_id,sticker_id))
        if event.type == "postback": 
            response = service_requester.post_store_search(event)
            line_response.push(data=response.content)

