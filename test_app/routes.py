from flask import render_template, request
from test_app import app
from test_app.forms import PayForm
from .pay_methods import method_other_pay, method_bill, method_pay



@app.route('/', methods=['GET', 'POST'])
def form():
    form = PayForm()
    if request.method == 'POST':
        if request.form['currency'] == 'USD':
            return method_bill(request)

        elif request.form['currency'] == 'EUR':
            return method_pay(request)

        else:
            return method_other_pay(request)

    return render_template('form.html', form=form)

