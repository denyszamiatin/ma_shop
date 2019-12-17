from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/catalogue')
def catalogue():
    return render_template("catalogue.html")


@app.route('/product')
def product():
    return render_template("product.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/news')
def news():
    return render_template("news.html")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/registration')
def registration():
    return render_template("registration.html")


@app.route('/product_comments')
def product_comments():
    return render_template("product_comments.html")


if __name__ == '__main__':
    app.run(debug=True)
