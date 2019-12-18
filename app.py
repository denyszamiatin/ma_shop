import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from db_utils.config import DATABASE
from news.news import get_all_news
from users import validation, user

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "sadasdasdasd"
con = psycopg2.connect(**DATABASE)


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
    data = get_all_news(con)
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
                user.add(con, first_name, second_name, email, password)
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


if __name__ == '__main__':
    app.run(debug=True)
