from flask import Flask, render_template, flash, request, json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests, time, json
from datetime import datetime

host = 'http://127.0.0.1:5000'
registry_host = 'http://127.0.0.1:3000'
# host2 = 'http://0.0.0.0:5000'
# host3 = 'http://0.0.0.0:5001'
# hosts = [host2, host3]


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    id = TextField('id:', validators=[validators.required()])
    # name  = TextField('name:')
    # desc = TextField('desc:')
    # email = TextField('email:')
    # address = TextField('address:')

@app.route('/')
def index():
    return "<h1>272 Demo</h1>"

@app.route('/databaseTest', methods=['GET', 'POST'])
def databaseT():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        print (form.errors)
        if request.form['submit'] == 'Register Entity':
            res = requests.post(registry_host + '/entity', data={})
            flash('Entity id: ' + res.text)

        if request.form['submit'] == 'Get Entity Info':
            id = str(request.form.get('id1'))
            res = requests.get(registry_host + '/entity/' + id)
            flash('Entity info: ' + res.text)

        if request.form['submit'] == 'Delete Entity':
            id = str(request.form.get('id1'))
            res = requests.delete(registry_host + '/entity/' + id)
            flash('Entity info: ' + res.text)

        if request.form['submit'] == 'Create Product':
            res = requests.post(registry_host + '/product', data={})
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Product Info':
            id = str(request.form.get('id2'))
            res = requests.get(registry_host + '/product/'+id)
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Delete Product':
            id = str(request.form.get('id2'))
            res = requests.delete(registry_host + '/product/'+id)
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Create Transaction':
            sku = str(request.form.get('sku'))
            fr = str(request.form.get('from'))
            to = str(request.form.get('to'))
            quantity = float(request.form.get('quantity'))
            res = requests.post(host + '/txns', data={'quantity': quantity, 'created_at_utc': time.time(), 'from_legal_entity': fr, 'to_legal_entity': to, 'product_sku': sku})
            flash('Transaction id: ' + res.text)

        if request.form['submit'] == 'Show Blockchain':
            res = requests.get(host + '/chain')
            flash('Current Blockchain: ' + res.text)

    return render_template('hello.html', form=form)


@app.route('/blockchainTest', methods=['GET', 'POST'])
def blockchainT():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        print (form.errors)
        if request.form['submit'] == 'Register Nodes':
            node1 = request.form.get('node1')
            node2 = request.form.get('node2')
            hosts = [node1, node2]
            node3 = request.form.get('node2re')
            res = requests.post(node3 + '/nodes/register', json={'nodes': hosts})
            flash('Register nodes on ' + node3 + ': ' + res.text)

        if request.form['submit'] == 'Get Node Info':
            info = request.form.get('node3')
            res = requests.get(info + '/chain')
            flash('Node info: ' + res.text)

        if request.form['submit'] == 'Register Entity':
            res = requests.post(registry_host + '/entity', data={})
            flash('Entity id: ' + res.text)

        if request.form['submit'] == 'Get Entity Info':
            id = str(request.form.get('id1'))
            res = requests.get(registry_host + '/entity/' + id)
            flash('Entity info: ' + res.text)

        if request.form['submit'] == 'Create Product':
            res = requests.post(registry_host + '/product', data={})
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Product Info':
            id = str(request.form.get('id2'))
            res = requests.get(registry_host + '/product/'+id)
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Delete Product':
            id = str(request.form.get('id2'))
            res = requests.delete(registry_host + '/product/'+id)
            flash('Product info: ' + res.text)

        if request.form['submit'] == 'Create Transaction':
            node2w = str(request.form.get('note2w'))
            sku = str(request.form.get('sku'))
            fr = str(request.form.get('from'))
            to = str(request.form.get('to'))
            quantity = float(request.form.get('quantity'))
            res = requests.post(node2w + '/txns', data={'quantity': quantity, 'created_at_utc': time.time(), 'from_legal_entity': fr, 'to_legal_entity': to, 'product_sku': sku})
            flash('Transaction id: ' + res.text)


    return render_template('hello2.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
