import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_bootstrap import Bootstrap

from db_utils.config import DATABASE
from news import news_
from users import validation, user
from products import products

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = ""


@app.before_request
def get_db():
    if not hasattr(g, 'db'):
        g.db = psycopg2.connect(**DATABASE)


@app.teardown_request
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/catalogue')
def catalogue():

    return render_template("catalogue.html")


@app.route('/categories')
def categories():
    return render_template("categories.html")


@app.route('/product')
def product():
    return render_template("product.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/news')
def news():
    data = news_.get_all(g.db)
    return render_template("news.html", data=data)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/registration', methods=("GET", "POST"))
def registration():
    message = ""
    if request.method == "POST":
        first_name = request.form.get("first_name", "")
        second_name = request.form.get("second_name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if validation.register_form_validation(first_name, second_name, email, password):
            try:
                user.add(g.db, first_name, second_name, email, password)
                flash("Registration was successful")
                return redirect(url_for('index'))
            except psycopg2.errors.UniqueViolation:
                message = f"User with email: {email} already exist"
        else:
            message = "Something wrong, check form"

    return render_template("registration.html", message=message)


@app.route('/product_comments')
def product_comments():
    return render_template("product_comments.html")


@app.route('/admin/add_product', methods=("GET", "POST"))
def add_product():
    if request.method == "POST":
        product_name = request.form.get("product_name", "")
        price = request.form.get("price", "")
        product_category = request.form.get("product_category", "")
        # img = request.form.get("img", "")
        products.add_product(g.db, product_name, price, product_category)
    return render_template("add_product.html")


if __name__ == '__main__':
    app.run(debug=True)
