from hashlib import sha256
import os
from random import choice
from string import digits
from test_app import db
from .models import PayRecord


def calculate_sha_256(*args, **kwargs):
    res = ''
    for items in args:
        for item in items:
            if items.index(item) == len(items) - 1:
                res += str(item)
            else:
                res += str(item) + ':'
    
    res_with_secret_key = res + kwargs['secretKey']
    result = sha256(f'{res_with_secret_key}'.encode('utf-8')).hexdigest()
    return result


def generate_order_id():
    order_id = ''.join([str(choice(digits)) for i in range(10)])
    return order_id


def save_to_db(currency, amount, description, shop_order_id):
    pay_record = PayRecord(currency=currency, amount=amount, description=description, shop_order_id=shop_order_id)

    if not os.path.exists('../test.db'):
        db.create_all()

    db.session.add(pay_record)
    db.session.commit()