from typing import Set, List
import json, os, copy


class StoreMessenger:
    """
    Skeleton class to implement LINE message format for location search
    """

    def __init__(self):
        FLEX_TEMPLATE = './message/flex_message.json'
        CONTENT_TEMPLATE = './message/bubble_message.json'
        FALLBACK_TEMPLATE = './message/fallback.json'
        BADGE_TEMPLATE = './message/badge_icon.json'
        BUTTON_TEMPLATE = './message/add_line_button.json'
        
        with open(FLEX_TEMPLATE, 'r') as f: self.line_flex_template = f.read()
        with open(CONTENT_TEMPLATE, 'r') as f: self.content_template = f.read()
        with open(FALLBACK_TEMPLATE, 'r') as f: self.fallback_template = f.read()
        with open(BADGE_TEMPLATE, 'r') as f: self.badge_template = f.read()
        with open(BUTTON_TEMPLATE, 'r') as f: self.add_line_button_template = f.read()

    def get_content(self, name:str, tel:str, address:str, lineOA:str,
                origin_lat:float, origin_lng:float, store_lat:float, store_lng:float, 
                AC:str, FM:str, FP:str, GP:str, KS:str, SP:str, VF:str, XT:str) -> Set:
        """
        Populate carousel content for LINE messenger

        :param kwargs:
        :return:
        """
        msg_template = copy.deepcopy(self.content_template)
        msg_template = msg_template.replace('<:name>', name).replace('<:tel>', tel).replace('<:address>', address)
        msg_template = msg_template.replace('<:origin_lat>', str(origin_lat)).replace('<:origin_lng>', str(origin_lng))
        msg_template = msg_template.replace('<:store_lat>', str(store_lat)).replace('<:store_lng>', str(store_lng))
        msg = json.loads(msg_template)

        # badge
        badges = []
        badge_list = ['AC', 'FM', 'FP', 'GP', 'KS', 'SP', 'VF', 'XT']
        for product_type in badge_list:
            if eval(f'{product_type}==str(1)'):
                badge_item = copy.deepcopy(self.badge_template)
                badge_item = badge_item.replace('<:product_type>',product_type)
                badges.append(json.loads(badge_item))
        
        msg['body']['contents'][1]['contents'][0]['contents'] = badges

        if len(lineOA)>0:
            add_line_button = copy.deepcopy(self.add_line_button_template).replace('<:lineOA>', lineOA)
            msg['footer']['contents'].insert(0, json.loads(add_line_button))

        return msg
    
    def get_line_message(self, user_id: str, contents: List, latitude: float, longitude: float):
        """
        Populate final LINE message which to be replied by chatbot engine

        :param user_id:
        :param contents:
        :param latitude:
        :param longitude:
        :return:
        """
        msg = copy.deepcopy(self.line_flex_template)
        msg = msg.replace('<:user_id>', user_id)
        msg = json.loads(msg)
        msg['messages'][0]['contents']['contents'] = contents
        return msg
    
    def get_fallback(self, user_id: str):
        """
        Return fallback message for LINE messenger

        :param user_id:
        :param latitude:
        :param longitude:
        :return:
        """
        msg = copy.deepcopy(self.fallback_template)
        msg = msg.replace('<:user_id>', user_id)
        return json.loads(msg)