import io
import os
import psycopg2
from PIL import Image

from flask import render_template, request, redirect, url_for, flash, g, session, send_file
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from app.db_utils.config import DATABASE
from cart import cart
from comments import comments
from errors import errors
from marks import mark
from product_categories import product_categories, category_validation
from products import products
from users import validation
from . import app
from app.db_utils.config import basedir
from .forms import *
from .models import *


@app.before_request
def get_db():
    if not hasattr(g, 'db'):
        g.db = psycopg2.connect(**DATABASE)


@app.teardown_request
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/image/<ln>')
def image(ln):
    sn = products.get_product_image(g.db, ln)
    return send_file(io.BytesIO(sn), mimetype='image/jpeg')


@app.route('/')
def index():
    email = ''
    if 'user_id' in session:
        user_ = Users.query.filter_by(id=session['user_id']).first()
        email = user_.email
    return render_template("index.html", email=email)


@app.route('/catalogue')
def catalogue():
    return render_template("catalogue.html")


@app.route('/product/product_description/<product_id>', methods=("GET", "POST"))
def show_product(product_id):
    avg_mark = mark.get_average(g.db, product_id)
    with g.db.cursor() as cursor:
        cursor.execute(f"select id, name, price, image from products where id = '{product_id}'")
        prod_data = cursor.fetchone()
        comment = ""
        if request.method == "POST":
            comment = request.form.get("comment", "")
            if 'user_id' not in session:
                flash("Please log in for leaving your comment")
                return redirect(url_for('login'))
            else:
                comments.add(g.db, product_id, session['id_user'], comment)
        return render_template("product_description.html", data=prod_data, comment=comment, avg_mark=avg_mark)


@app.route('/product/add_to_cart/<product_id>', methods=("GET", "POST"))
def add_to_cart(product_id):
    if request.method == "POST":
        if session["user_id"]:
            cart.add(g.db, session["user_id"], product_id)
    return redirect(url_for("categories"))


@app.route('/cart', methods=("GET", "POST"))
def cart_call():
    cart_items = {}
    if "user_id" in session:
        if request.method == "POST":
            cart.delete(g.db, int(session["user_id"]), int(request.form.get("delete_item", "")))
        for product_id in cart.get_all(g.db, int(session["user_id"])):
            if product_id not in cart_items:
                name, price = products.get_for_cart(g.db, product_id)
                cart_items[product_id] = {
                    "product_id": product_id,
                    "name": name,
                    "price": price,
                    "pieces": 1
                }
            else:
                cart_items[product_id]["pieces"] += 1
    return render_template("cart.html", cart_items=cart_items)


@app.route('/news')
def news():
    all_news = News.query.all()
    users = Users.query.filter(Users.id == News.id_user).all()
    return render_template("news.html", news=all_news, users=users)


@app.route('/comments_list/<product_id>', methods=("GET", "POST"))
def comments_list(product_id):
    all_comments = comments.get(g.db, product_id)
    return render_template("comments_list.html", comments=all_comments)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/logout')
def logout():
    if "user_id" in session:
        session.pop("user_id")
        flash("You logged out")
        return redirect(url_for('index'))
    else:
        flash("You are not logged in")
        return redirect(url_for('index'))


@app.route('/login', methods=("GET", "POST"))
def login():
    message = ""
    form = UserLoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        if validation.login_form_validation(email, password):
            try:
                user_ = Users.query.filter_by(email=email).first()
                if check_password_hash(user_.password, password):
                    session['user_id'] = user_.id
                    flash("You are logged")
                    return redirect(url_for('index'))
                else:
                    message = "Wrong password"
            except AttributeError:
                message = "Wrong email"
        else:
            message = "Something wrong, check form"

    return render_template("login.html", form=form, message=message)


@app.route('/registration', methods=("GET", "POST"))
def registration():
    message = ""
    form = UserRegistrationForm()
    if request.method == "POST":
        first_name = form.first_name.data
        second_name = form.second_name.data
        email = form.email.data
        password = form.password.data
        if validation.register_form_validation(first_name, second_name, email, password):
            try:
                user_ = Users(first_name, second_name, email, password)
                db.session.add(user_)
                db.session.commit()
                flash("Registration was successful")
                return redirect(url_for('index'))
            except IntegrityError:
                message = f"User with email: {email} already exist"
        else:
            message = "Something wrong, check form"

    return render_template("registration.html", message=message, form=form)


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
            except errors.StoreError:
                message = f"Category with name: {category_name} already exist"
        else:
            message = "Something wrong, check form"

    return render_template("add_category.html", message=message, category_name=category_name)


@app.route('/admin')
def index_admin():
    return render_template("index_admin.html")


@app.route('/admin/add_product', methods=("GET", "POST"))
def add_product():
    """function for add product in database"""
    form = AddProductForm()
    all_categories = ProductCategories.query.all()
    form.category_id.choices = [(int(category.id), category.name) for category in all_categories]
    if request.method == "POST" and form.validate():
        product = Products(name=form.name.data,
                           price=form.price.data,
                           description=form.description.data,
                           category_id=form.category_id.data)
        db.session.add(product)
        db.session.commit()

        def save_image_and_thumbnail():
            """getting image from form and save with name = product.id
            :return (url image, url thumbnail)"""
            image = form.image.data
            imagename = f"{product.id}.{secure_filename(image.filename).split('.')[-1]}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
            image.save(os.path.join(basedir, image_path))
            image = Image.open(image)
            image.thumbnail(app.config['THUMBNAIL_SIZE'])
            thumbnail_name = imagename.split('.')
            thumbnail_name = f"{''.join(thumbnail_name[:-1])}_thumbnail.{thumbnail_name[-1]}"
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_name)
            image.save(os.path.join(basedir, thumbnail_path))
            return (image_path, thumbnail_path)

        images_path = save_image_and_thumbnail()
        product.image, product.thumbnail = images_path
        db.session.commit()

    return render_template("add_product.html", form=form)


@app.route('/categories/<string:category_id>', methods=("GET", "POST"))
def categories(category_id):
    all_categories = ProductCategories.query.all()
    if request.method == "POST":
        if session["user_id"]:
            cart.add(g.db, session["user_id"], request.form.get("add_to_cart", ""))
    if category_id == "all":
        all_products = Products.query.all()
    else:
        all_products = Products.query.filter_by(category_id=category_id).all()
    return render_template("catalogue.html", categories=all_categories, products=all_products)


@app.route('/admin/add_news', methods=("GET", "POST"))
def add_news():
    if request.method == 'POST':
        title = request.form.get('title', '')
        post = request.form.get('post', '')
        id_user = session.get('user_id', 1)
        try:
            new_news = News(title=title, post=post, id_user=id_user)
            db.session.add(new_news)
            db.session.commit()
            flash('News was successfully added to db')
        except orm.exc.NoResultFound:
            flash('News wasn\'t added to db')
        return redirect(url_for('news'))
    form = NewsForm()
    return render_template('add_news.html', form=form)


@app.route('/admin/edit_category/<string:category_id>', methods=("GET", "POST"))
def edit_category(category_id):
    category = product_categories.read(g.db, category_id)
    if request.method == "POST":
        new_name = request.form.get("new_name", "")
        try:
            product_categories.update(g.db, category_id, new_name)
            flash("Category updated")
            return redirect(url_for('index_admin'))
        except psycopg2.errors.UniqueViolation:
            flash(f"Category {new_name} already exist")
        except errors.StoreError:
            flash("Something wrong, check form")
    return render_template("edit_category.html", category=category)


@app.route("/admin/confirm_delete_category/<category_id>", methods=("GET", "POST"))
def confirm_delete_category(category_id):
    category_ = product_categories.read(g.db, category_id)
    return render_template("confirm_delete_category.html", id=category_id, category=category_)


@app.route("/admin/confirm_delete_category/delete/<category_id>", methods=("GET", "POST"))
def delete_category(category_id):
    product_categories.delete(g.db, category_id)
    flash("Deleted")
    return redirect(url_for('categories_list'))


@app.route('/admin/products_list', methods=("GET", "POST"))
def products_list():
    all_products = products.get_all_2(g.db)
    return render_template("products_list.html", all_products=all_products)


@app.route('/admin/edit_product/<string:product_id>', methods=("GET", "POST"))
def edit_product(product_id):
    product = products.get_product_2(g.db, product_id)
    categories = product_categories.get_all(g.db)
    if request.method == "POST":
        id = request.form.get("product_id", "")
        name = request.form.get("product_name", "")
        price = request.form.get("price", "")
        img = request.files['img'].read()
        category = request.form.get("category", "")
        try:
            products.edit_product_2(g.db, id, name, price, category, img)
            flash("Product edited")
            return redirect(url_for('products_list'))
        except errors.StoreError:
            flash("Smth wrong, pls try again")
    return render_template("edit_product.html", product=product, categories=categories)


@app.route('/admin/delete_news', methods=("GET", "POST"))
def delete_news():
    all_news = News.query.all()
    users = Users.query.filter(Users.id == News.id_user).all()
    return render_template("delete_news.html", news=all_news, users=users)


@app.route('/admin/delete_news/<string:news_id>', methods=("GET", "POST"))
def delete_news_id(news_id):
    News.query.filter(News.id == news_id).delete()
    db.session.commit()
    flash('News was successfully deleted from db')
    return redirect(url_for('delete_news'))


@app.route('/admin/edit_news', methods=("GET", "POST"))
def edit_news():
    all_news = News.query.all()
    users = Users.query.filter(Users.id == News.id_user).all()
    return render_template("edit_news.html", news=all_news, users=users)


@app.route('/admin/edit_news/<string:news_id>', methods=("GET", "POST"))
def edit_news_id(news_id):
    post = News.query.filter(News.id == news_id).first()
    if request.method == 'POST':
        form = NewsForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        flash('News was successfully updated in db')
        return redirect(url_for('edit_news'))
    form = NewsForm(obj=post)
    return render_template('edit_news_id.html', post=post, form=form)


@app.route("/admin/delete_product", methods=("GET", "POST"))
def delete_product():
    all_products = products.get_all(g.db)
    return render_template("delete_product.html", products=all_products)


@app.route("/admin/delete_confirm/<product_id>", methods=("GET", "POST"))
def delete_confirm(product_id):
    product_ = products.get_product(g.db, product_id)
    return render_template("delete_confirm.html", id=product_id, product=product_)


@app.route("/admin/delete_confirm/delete/<product_id>", methods=("GET", "POST"))
def delete(product_id):
    products.delete_product(g.db, product_id)
    flash("Deleted")
    return redirect(url_for('products_list'))


@app.route('/product/set_mark/<string:product_id>', methods=("GET", "POST"))
def set_product_mark(product_id):
    if request.method == "POST":
        product_mark = request.form.get("mark", "")
        if 'user_id' not in session:
            flash("Please log in for leaving your mark")
            return redirect(url_for('login'))
        else:
            if int(product_mark) <= 0 or int(product_mark) > 5:
                flash("Mark should be between 1 and 5")
            else:
                mark.add(g.db, session['id_user'], product_id, product_mark)
                flash("Your mark has been added successfully")
        return redirect(url_for('product'))


"""@app.route('/cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = products.get_product(product_id)
    cart_item = CartItem(product=product)
    db.session.add(cart_item)
    db.session.commit()
    return render_tempate('home.html', product=products)"""


@app.route('/admin/categories_list', methods=("GET", "POST"))
def categories_list():
    all_categories = product_categories.get_all(g.db)
    return render_template("categories_list.html", all_categories=all_categories)
