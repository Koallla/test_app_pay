import copy
from config import keys_required_dict, base_data_dict
from flask import redirect
from test_app.forms import currency_dict
from .helpers import generate_order_id, save_to_db, calculate_sha_256

import requests

def method_bill(request):
    data_dict = copy.deepcopy(base_data_dict)
    description = request.form['description']
    amount = request.form['amount']
    currency = currency_dict[request.form['currency']]
    shop_order_id = generate_order_id()

    data_dict['description'] = description
    data_dict['payer_currency'] = currency
    data_dict['shop_amount'] = amount
    data_dict['shop_currency'] = currency
    data_dict['shop_order_id'] = shop_order_id

    save_to_db(currency, amount, description, shop_order_id)

    keys = keys_required_dict[request.form['currency']]
    keys_sort = sorted(keys)
    keys_sort_value = []
    for key in keys_sort:
        keys_sort_value.append(data_dict[key])
    
    data_dict['sign'] = calculate_sha_256(keys_sort_value, secretKey=data_dict['secretKey'])

    response = requests.post('https://core.piastrix.com/bill/create', json=data_dict)
    r = response.json()
    if r['result']:
        url = r['data']['url']
        return redirect(url)
    else:
        return r['message']

def method_pay(request):
    data_dict = copy.deepcopy(base_data_dict)
    description = request.form['description']
    currency = currency_dict[request.form['currency']]
    amount = request.form['amount']
    shop_id = data_dict['shop_id']
    shop_order_id = generate_order_id()

    data_dict['description'] = request.form['description']
    data_dict['currency'] = currency
    data_dict['amount'] = amount
    data_dict['shop_order_id'] = shop_order_id


    save_to_db(currency, amount, description, shop_order_id)

    keys = keys_required_dict[request.form['currency']]
    keys_sort = sorted(keys)
    keys_sort_value = []
    for key in keys_sort:
        keys_sort_value.append(data_dict[key])
    
    sign = calculate_sha_256(keys_sort_value, secretKey=data_dict['secretKey'])
    data_dict['sign'] = sign

    return f'<form name="Pay" method="post" action="https://pay.piastrix.com/ru/pay" accept-charset="UTF-8"> <input type="hidden" name="amount" value="{amount}"/> <input type="hidden" name="currency" value="{currency}"/> <input type="hidden" name="shop_id" value="{shop_id}"/> <input type="hidden" name="sign" value="{sign}"/> <input type="hidden" name="shop_order_id" value="{shop_order_id}"/> <input type="submit" value="Подтвердить отправку платежа"/> <input type="hidden" name="description" value="Test invoice"/> </form>'

def method_other_pay(request):
    data_dict = copy.deepcopy(base_data_dict)
    description = request.form['description']
    currency = currency_dict[request.form['currency']]
    amount = request.form['amount']
    shop_order_id = generate_order_id()
    data_dict['description'] = description
    data_dict['currency'] = currency
    data_dict['amount'] = amount
    data_dict['shop_order_id'] = shop_order_id

    save_to_db(currency, amount, description, shop_order_id)

    keys = keys_required_dict[request.form['currency']]
    keys_sort = sorted(keys)
    keys_sort_value = []
    for key in keys_sort:
        keys_sort_value.append(data_dict[key])
    

    sign = calculate_sha_256(keys_sort_value, secretKey=data_dict['secretKey'])
    data_dict['sign'] = sign

    
    response = requests.post('https://core.piastrix.com/invoice/create', json=data_dict)
    r = response.json()
    
    # Можно оптимизировать
    if r['result']:
        method = r['data']['method']
        action_url = r['data']['url']
        ac_account_email = r['data']['data']['ac_account_email']
        ac_sci_name = r['data']['data']['ac_sci_name']
        ac_amount = r['data']['data']['ac_amount']
        ac_currency = r['data']['data']['ac_currency']
        ac_order_id = r['data']['data']['ac_order_id']

        return f'<form method="{method}" action="{action_url}"> <input type="hidden" name="ac_account_email" value="{ac_account_email}" /> <input type="hidden" name="ac_sci_name" value="{ac_sci_name}"/> <input type="hidden" name="ac_amount" value="{ac_amount}"/> <input type="hidden" name="ac_currency" value="{ac_currency}"/> <input type="hidden" name="ac_order_id" value="{ac_order_id}"/> <input type="submit" value="Подтвердить отправку платежа"/> </form>'