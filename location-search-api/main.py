from flask import jsonify
from system import Configurator
from location import StoreFinder
from messenger import StoreMessenger
from typing import List, Set
import json, os, sys


def find_seven_store(request):
    ''' Find nearest merchants according to given latitude and longtitude. '''
    print('INFO:', {'request': request.json})
    config = Configurator('./private/config.json')
    finder = StoreFinder(config)
    msg = StoreMessenger()
    
    #region get_postback_value
    user_id = request.json['source']['userId']
    data = request.json['postback']['data']
    kv = dict(val.split('=') for val in data.split('&'))
    product_type = kv['ProductType']
    latitude = kv['latitude']
    longitude = kv['longitude']
    print(product_type,latitude,longitude)
    #endregion get_postback_value

    # try:
    result_set = finder.find_shops(current_lat=float(latitude), current_long=float(longitude), max_distance=5000, product_type=product_type)

    #region rendering flex message
    if len(result_set) > 0:
        contents = []
        for shop in result_set:      
            content = msg.get_content(
                name=shop['name'], tel=shop['tel'], address=shop['address'], lineOA=shop['lineOA'],
                origin_lat=float(latitude), origin_lng=float(longitude), store_lat=shop['lat'], store_lng=shop['lng'],
                AC=shop['AC'], FM=shop['FM'], FP=shop['FP'], GP=shop['GP'], KS=shop['KS'], SP=shop['SP'], VF=shop['VF'], XT=shop['XT']
            )
            contents.append(content)
        response = msg.get_line_message(user_id=user_id, contents=contents, latitude=float(latitude), longitude=float(longitude))
    #endregion rendering flex message
    else: 
        response = msg.get_fallback(user_id=user_id)
    print('INFO:', {'response': response})
    return jsonify(response)
    # except (KeyError, ValueError) as e: 
    #     print('WARN:', {'response': str(e)})
    #     return jsonify({'code': 400, 'error': str(e), 'message':'Please validate input data.'})
    # except Exception as e:
    #     print('WARN:', json.dumps({'response': str(e)}))
    #     return jsonify({'code': 400, 'message': str(e)})
