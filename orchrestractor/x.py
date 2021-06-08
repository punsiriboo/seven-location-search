from line import LineResponse
from system import Configurator
configurator = Configurator("private/config.json")
print(configurator.get('line.access_token'))
line_response = LineResponse(configurator.get('line.access_token'))

import json
with open('message/template_ask_product_type.json') as f: 
    msg_text = f.read().replace("<:user_id>","U1153d6b653f927eb10478a394427aef7").replace("<:latitude>",str(1)).replace("<:longitude>",str(1))
    line_response.push(json.dumps(json.loads(msg_text)))