from flask import Flask, render_template

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/corporate')
def corporate():
    return render_template('corporate.html')


@app.get('/fees')
def fees():
    return render_template('fees.html')


@app.get('/security')
def security():
    return render_template('security.html')


@app.get('/market')
def market():
    return render_template('market.html')


@app.get('/wallet')
@app.get('/balance')
def balance():
    return render_template('balance.html')


@app.get('/sing-up')
@app.get('/register')
def register():
    return render_template('sing-up.html')


@app.get('/login')
def login():
    return render_template('login.html')


@app.get('/about')
def about():
    return render_template('about.html')


@app.get('/privacy')
def privacy():
    return render_template('privacy.html')


@app.get('/termofuse')
def termofuse():
    return render_template('termofuse.html')


@app.get('/affiliate')
def affiliate():
    return render_template('affiliate.html')


@app.get('/smart')
def smart():
    return render_template('smart.html')


@app.get('/referral')
def referral():
    return render_template('referral.html')


@app.get('/faq')
def faq():
    return render_template('faq.html')


@app.get('/support')
def support():
    return render_template('support.html')


@app.get('/livetrade')
def livetrade():
    return render_template('livetrade.html')


@app.get('/exchange')
def exchange():
    return render_template('exchange.html')


@app.get('/orders')
def orders():
    return render_template('orders.html')


@app.get('/history')
def history():
    return render_template('history.html')


@app.get('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run(debug=True)
