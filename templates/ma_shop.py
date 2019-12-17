from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


def catalogue():
    return render_template("catalogue.html")


def product():
    return render_template("product.html")


def cart():
    return render_template("cart.html")


def news():
    return render_template("news.html")


def contacts():
    return render_template("contacts.html")


def login():
    return render_template("login.html")


def registration():
    return render_template("registration.html")


def product_comments():
    return render_template("product_comments.html")


if __name__ == '__main__':
    app.run(debug=True)

