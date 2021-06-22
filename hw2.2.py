import datetime
import json


def write_order_to_json(item='none', quantity='none', price='none', buyer='none', date='none'):
    json_dict = dict(item=item, quantity=quantity, price=price, buyer=buyer, date=date)

    for key, item in json_dict.items():
        if item is not str and item is not int and item is not bool:
            json_dict[key] = str(item)

    with open('orders.json', 'w', encoding='utf-8') as json_doc:
        json.dump(json_dict, json_doc, indent=4)


write_order_to_json('laptop', '2', '50000', 'Ekaterina', datetime.datetime.now())
