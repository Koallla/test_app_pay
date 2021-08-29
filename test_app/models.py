from datetime import datetime
from test_app import db


class PayRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(50))
    amount = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500))
    shop_order_id = db.Column(db.String(256))

    def __repr__(self):
        return 'Amount {}'.format(self.amount)
