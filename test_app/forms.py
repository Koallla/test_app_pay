from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length

currency_list = ['EUR', 'USD', 'RUB']
currency_dict = {'EUR': '978', 'USD': '840', 'RUB': '643'}

class PayForm(FlaskForm):
    amount = IntegerField('Сумма оплаты', validators=[DataRequired()])
    currency = SelectField('Валюта оплаты', validators=[DataRequired()], choices=currency_list)
    description = TextAreaField('Описание товара', validators=[Length(min=0, max=500)])
    sign = StringField('Подпись', validators=[DataRequired()])
    submit = SubmitField('Оплатить')