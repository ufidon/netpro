#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_insecure.py
# A poorly-written and profoundly insecure payments application.
# (Not the fault of Flask, but of how we are choosing to use it!)

# The application uses the Flask web framework to take care of 
# the basics of operating as a Python web application:
# 1. answering 404 for pages that the application does not define, 
# 2. parsing data from HTML forms  
# 3. making it easy to compose correct HTTP responses containing 
#   either HTML text from one of its templates 
#   or a redirect to another URL
# 4. styling documents with Jinja2

# The weaknesses are all mistakes in its data processing
# so HTTPS will not help, why?
# vulnerable to many of the most important attack vectors 

import bank
from flask import Flask, redirect, request, url_for
from jinja2 import Environment, PackageLoader

app = Flask(__name__)
get = Environment(loader=PackageLoader(__name__, 'templates')).get_template

# logging in and logging out is 
# the creation and deletion of a cookie
# when present in subsequent requests, marks them as
# belonging to a particular authenticated user

@app.route('/login', methods=['GET', 'POST'])
def login():
    # request.form.get returns a default of '' if a key is missing
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('brandon', 'atigdng'), ('sam', 'xyzzy')]:
            response = redirect(url_for('index'))
            response.set_cookie('username', username)
            return response
    return get('login.html').render(username=username)

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.set_cookie('username', '')
    return response

# The following two pages protect themselves from unauthorized users 
# both by looking for the cookie and
# redirecting back to the login page without a correct value

@app.route('/')
def index():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    # pulls the current user’s payments from the database
    payments = bank.get_payments_of(bank.open_database(), username)

    # fill the template index.html
    # a flash message displayed at the top of the page 
    # to show intermediary operation results
    # such as http://example.com/?flash=Payment+successful
    return get('index.html').render(payments=payments, username=username,
        flash_messages=request.args.getlist('flash'))

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    account = request.form.get('account', '').strip()
    dollars = request.form.get('dollars', '').strip()
    memo = request.form.get('memo', '').strip()
    complaint = None
    if request.method == 'POST':
        if account and dollars and dollars.isdigit() and memo:
            db = bank.open_database()
            bank.add_payment(db, username, account, dollars, memo)
            db.commit()
            return redirect(url_for('index', flash='Payment successful'))
        complaint = ('Dollars must be an integer' if not dollars.isdigit()
                     else 'Please fill in all three fields')
    return get('pay.html').render(complaint=complaint, account=account,
                                  dollars=dollars, memo=memo)

if __name__ == '__main__':
    # enabled debug mode can restart Flask and reload the application for updates
    app.debug = True
    app.run()
