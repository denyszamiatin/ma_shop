import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_bootstrap import Bootstrap

from db_utils.config import DATABASE
from news import news_
from users import validation, user
from products import products
from product_categories import product_categories, category_validation
from errors import errors

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "3123123123"


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


@app.route('/login', methods=("GET", "POST"))
def login():
    message = email = ""
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if validation.login_form_validation(email, password):
            try:
                session['user_id'] = user.login(g.db, email, password)
                flash("You are logged")
                return redirect(url_for('index'))
            except errors.StoreError:
                message = "Wrong password or email"

        else:
            message = "Something wrong, check form"

    return render_template("login.html", message=message, email=email)


@app.route('/registration', methods=("GET", "POST"))
def registration():
    message = first_name = second_name = email = ""
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

    return render_template("registration.html", message=message, first_name=first_name, second_name=second_name, email=email)


@app.route('/admin/add_category', methods=("GET", "POST"))
def add_category():
    category_name = message = ''
    if request.method == "POST":
        category_name = request.form.get("category_name", "")
        if category_validation.validator(category_name):
            try:
                product_categories.create(g.db, category_name)
                flash("Category added")
                return redirect(url_for('index_admin'))
            except psycopg2.errors.UniqueViolation:
                message = f"Category with name: {category_name} already exist"
        else:
            message = "Something wrong, check form"

    return render_template("add_category.html", message=message, category_name=category_name)


@app.route('/product_comments')
def product_comments():
    return render_template("product_comments.html")


@app.route('/admin')
def index_admin():
    return render_template("index_admin.html")


@app.route('/admin/add_product', methods=("GET", "POST"))
def add_product():
    all_categories = product_categories.get_all(g.db)
    if request.method == "POST":
        product_name = request.form.get("product_name", "")
        price = request.form.get("price", "")
        img = request.files['img'].read()
        category = request.form.get("category")
        products.add_product(g.db, product_name, price, img, category)

    return render_template("add_product.html", all_categories=all_categories)


@app.route('/categories')
def categories():
    all_categories = product_categories.get_all(g.db)
    all_products = products.get_all(g.db)

    return render_template("categories.html", categories=all_categories, products=all_products)


@app.route('/admin/add_news', methods=("GET", "POST"))
def add_news():
    title, post = '', ''
    if request.method == "POST":
        title = request.form.get("title", "")
        post = request.form.get("post", "")
        id_user = session.get('user_id', 1)
        news_.add(g.db, title, post, id_user)
        if not title or not post:
            flash('All fields must be filled in')
    return render_template('add_news.html', title=title, post=post)


@app.route('/admin/delete_category', methods=("GET", "POST"))
def delete_category_list():
    all_categories = product_categories.get_all(g.db)
    return render_template("delete_category.html", all_categories=all_categories)


@app.route('/admin/delete_category/<string:category_id>', methods=("GET", "POST"))
def delete_category(category_id):
    product_categories.delete(g.db, category_id)
    return redirect(url_for('delete_category_list'))


# @app.route('/cart/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):
#
#     product = Product.query.filter(Product.id == product_id)
#     cart_item = CartItem(product=product)
#     db.session.add(cart_item)
#     db.session.commit()
#
#     return render_tempate('home.html', product=products)


if __name__ == '__main__':
    app.run(debug=True)