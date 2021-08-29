import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-task'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False




keys_required_dict = {
    'EUR': ['amount', 'currency', 'shop_id', 'shop_order_id'],
    'USD': ['shop_amount', 'shop_currency', 'shop_id', 'shop_order_id', 'payer_currency'],
    'RUB': ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']
}

base_data_dict = {
    'shop_id': '5',
    'secretKey': 'SecretKey01',
    'payway': 'advcash_rub'
    }