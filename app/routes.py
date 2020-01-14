import io
from pathlib import Path

import psycopg2
from PIL import Image
from flask import render_template, request, redirect, url_for, flash, g, session, send_file, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from app.config import DATABASE, basedir, ITEMS_PER_PAGE
from cart import cart
from comments import comments
from errors import errors
from products import products
from users import validation
from .forms import *
from .models import *
from .login import login_required
from .breadcrumb import breadcrumb
from .api import *
from .send_mail import send_mail
from .registration_token import generate_confirmation_token, confirm_token


def save_image_and_thumbnail(image_data, product_id):
    """save image and image_thumbnail"""
    image = Image.open(image_data)
    rgb_im = image.convert('RGB')
    image_name = f"{product_id}.jpg"
    rgb_im.save(Path(basedir, app.config['UPLOAD_FOLDER'], image_name))
    rgb_im.thumbnail(app.config['THUMBNAIL_SIZE'])
    thumbnail_name = f"{product_id}_thumbnail.jpg"
    rgb_im.save(Path(basedir, app.config['UPLOAD_FOLDER'], thumbnail_name))


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
@breadcrumb('Home')
def index():
    return render_template("index.html")


def paging(items, page_template):
    next_url = url_for(page_template, page=items.next_num) \
        if items.has_next else None
    prev_url = url_for(page_template, page=items.prev_num) \
        if items.has_prev else None
    return next_url, prev_url


@app.route('/product/product_description/<product_id>', methods=("GET", "POST"))
def show_product(product_id):
    form = MarkForm()
    raw_avg = db.session.query(func.avg(Mark.rating)).filter(Mark.id_product == product_id).first()
    avg_mark = round(raw_avg[0], 2) if raw_avg[0] is not None else 'No marks'
    product = Products.query.filter_by(id=product_id).first()
    number_of_marks = len(Mark.query.filter_by(id_product=product_id).all())
    product_category = ProductCategories.query.get(product.category_id).name
    comment = ""
    if request.method == "POST":
        comment = request.form.get("comment", "")
        if 'user_id' not in session:
            flash("Please log in for leaving your comment")
            return redirect(url_for('login'))
        else:
            comments.add(g.db, product_id, session['id_user'], comment)
    return render_template("product_description.html", product=product, comment=comment, avg_mark=avg_mark, form=form,
                           number_of_marks=number_of_marks, product_category=product_category)


@app.route('/product/set_mark/<string:product_id>', methods=("GET", "POST"))
@login_required
def set_product_mark(product_id):
    form = MarkForm()
    new_mark = form.mark.data
    if Mark.query.filter_by(id_user=session['user_id'], id_product=product_id).first() is not None:
        db.session.query(Mark).filter(Mark.id_user == session['user_id'], Mark.id_product == product_id).\
            update({Mark.rating: new_mark})
        db.session.commit()
        flash("Your mark has been updated successfully")
    else:
        mark = Mark(session['user_id'], product_id, new_mark)
        db.session.add(mark)
        db.session.commit()
        flash("Your mark has been added successfully")
    return redirect(f'/product/product_description/{product_id}')


@app.route('/product/add_to_cart/<product_id>', methods=("GET", "POST"))
@login_required
def add_to_cart(product_id):
    if request.method == "POST":
        to_cart = Cart(id_user=session["user_id"], id_product=product_id)
        db.session.add(to_cart)
        db.session.commit()
    return redirect(url_for("get_catalogue"))


@app.route('/cart', methods=("GET", "POST"))
@login_required
@breadcrumb('Cart')
def cart_call():
    cart_items = {}
    items_qty = 0
    total_amount = 0
    if request.method == "POST":
        Cart.query.filter_by(id_user=session["user_id"], id_product=request.form.get("delete_item", "")).delete()
        db.session.commit()
    all_products = db.session.query(Cart.id_product, Products.name, Products.price)\
        .filter(Products.id == Cart.id_product, Cart.id_user == session["user_id"], Products.deleted == 'False').all()
    for item in range(len(all_products)):
        prod_id = all_products[item][0]
        if prod_id not in cart_items:
            name, price = all_products[item][1], all_products[item][2]
            cart_items[prod_id] = {
                "product_id": prod_id,
                "name": name,
                "price": price,
                "pieces": 1
            }
            cart_items[prod_id]["amount"] = cart_items[prod_id]["price"] * cart_items[prod_id]["pieces"]
        else:
            cart_items[prod_id]["pieces"] += 1
            cart_items[prod_id]["amount"] += cart_items[prod_id]["price"]
        total_amount += cart_items[prod_id]["price"]
        items_qty += 1
    return render_template("cart.html", cart_items=cart_items, items_qty=items_qty, total_amount=total_amount)


@app.route('/news')
@breadcrumb('News')
def news():
    page = request.args.get('page', 1, type=int)
    news = db.session.query(News) \
        .join(Users) \
        .add_columns(News.title, News.post, News.news_date, Users.first_name, Users.second_name) \
        .filter(Users.id == News.id_user).paginate(page, ITEMS_PER_PAGE, False)
    next_url, prev_url = paging(news, 'news')
    return render_template("news.html", news=news.items, next_url=next_url, prev_url=prev_url)


@app.route('/comments_list/<product_id>', methods=("GET", "POST"))
def comments_list(product_id):
    all_comments = comments.get(g.db, product_id)
    return render_template("comments_list.html", comments=all_comments)


@app.route('/contacts')
@breadcrumb('Contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/logout')
@login_required
def logout():
    session.pop("user_id")
    if "next_page" in session:
        session.pop("next_page")
    flash("You logged out")
    return redirect(url_for('index'))


@app.route('/login', methods=("GET", "POST"))
@breadcrumb('Login')
def login():
    message = ""
    form = UserLoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        try:
            user = Users.query.filter_by(email=email).first()
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                if 'next_page' in session:
                    return redirect(session["next_page"])
                flash("You are logged")
                return redirect(url_for("index"))
            else:
                message = "Wrong email or password"
        except AttributeError:
            message = "Wrong email or password"

    return render_template("login.html", form=form, message=message)


@app.route('/registration', methods=("GET", "POST"))
@breadcrumb('Registration')
def registration():
    message = ""
    form = UserRegistrationForm()
    if request.method == "POST":
        first_name = form.first_name.data
        second_name = form.second_name.data
        email = form.email.data
        password = form.password.data
        if validation.register_form_validation(first_name, second_name, password):
            try:
                if email == "admin@example.com":
                    user = Users(first_name, second_name, email, password, admin_role=True, confirmed=True)
                else:
                    user = Users(first_name, second_name, email, password, admin_role=False, confirmed=False)
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                flash(f"User with email: {email} already exist")
            token = generate_confirmation_token(email)
            confirm_url = app.config['SITE_URL'] + url_for('confirmation', token=token)
            subject = "Please confirm your email"
            try:
                send_mail(email, subject, confirm_url)
            except ConnectionRefusedError as error:
                print(error)
            flash('A confirmation email has been sent via email.', 'success')
            return redirect(url_for('index'))
        else:
            message = "Something wrong, check form"

    return render_template("registration.html", message=message, form=form)


@app.route('/confirm/<token>')
def confirmation(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))
    user = Users.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login'))

@app.route('/admin/add_category', methods=("GET", "POST"))
@login_required
def add_category():
    """Admin: add category"""
    form = CategoryForm()
    if request.method == "POST" and form.validate():
        category = ProductCategories(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category added")
        return redirect(url_for('categories_list'))
    return render_template("add_category.html", form=form)


@app.route('/admin')
def index_admin():
    return render_template("index_admin.html")


@app.route('/admin/add_product', methods=("GET", "POST"))
@login_required
def add_product():
    """function for add product in database"""
    form = AddProductForm()
    form.category_id.choices = [(int(category.id), category.name) for category in ProductCategories.query.all()]
    if request.method == "POST" and form.validate():
        product = Products(name=form.name.data,
                           price=form.price.data,
                           description=form.description.data,
                           category_id=form.category_id.data)
        db.session.add(product)
        db.session.commit()
        save_image_and_thumbnail(form.image.data, product.id)
        flash("Product added")
        return redirect(url_for('products_list'))
    return render_template("add_product.html", form=form)


@app.route('/catalogue/<category>', methods=("GET", "POST"))
@app.route('/catalogue', methods=("GET", "POST"))
@breadcrumb('Catalogue')
def get_catalogue(category="all"):
    categories = ProductCategories.query.all()
    existing_categories = [str(category.id) for category in categories]
    if category not in existing_categories and category != "all":
        abort(404)
    page = request.args.get('page', 1, type=int)
    products = Products.query.filter_by(deleted=False).paginate(page, ITEMS_PER_PAGE, False)
    if category != "all":
        products = Products.query.filter_by(category_id=category, deleted=False).paginate(page, ITEMS_PER_PAGE, False)
    next_url, prev_url = paging(products, 'get_catalogue')
    return render_template("catalogue.html", categories=categories,
                           products=products.items, next_url=next_url, prev_url=prev_url)


@app.route('/admin/add_news', methods=("GET", "POST"))
@login_required
def add_news():
    form = NewsForm()
    if request.method == 'POST':
        try:
            new_news = News(title=form.title.data, post=form.post.data, id_user=session['user_id'])
            db.session.add(new_news)
            db.session.commit()
            flash('News was successfully added to db.')
        except IntegrityError:
            flash('News wasn\'t added to db.')
        return redirect(url_for('news'))

    return render_template('add_news.html', form=form)


@app.route('/admin/edit_category/<string:category_id>', methods=("GET", "POST"))
@login_required
def edit_category(category_id):
    category = ProductCategories.query.filter_by(id=category_id).first()
    form = CategoryForm()
    if request.method == "POST":
        try:
            form.populate_obj(category)
            db.session.commit()
            flash("Category updated")
        except IntegrityError:
            flash('Category was not edited!!')
        return redirect(url_for('categories_list'))
    elif request.method == "GET":
        form = CategoryForm(formdata=request.form, obj=category)
    return render_template("edit_category.html", form=form, category=category)


@app.route("/admin/confirm_delete_category/<category_id>", methods=("GET", "POST"))
@login_required
def confirm_delete_category(category_id):
    category_ = ProductCategories.query.filter_by(id=category_id).first()
    return render_template("confirm_delete_category.html", category=category_)


@app.route("/admin/confirm_delete_category/delete/<category_id>", methods=("GET", "POST"))
@login_required
def delete_category(category_id):
    ProductCategories.query.filter_by(id=category_id).delete()
    db.session.commit()
    flash("Deleted")
    return redirect(url_for('categories_list'))


@app.route('/admin/products_list', methods=("GET", "POST"))
@login_required
def products_list():
    page = request.args.get('page', 1, type=int)
    products = Products.query.order_by(Products.id).paginate(page, ITEMS_PER_PAGE, False)
    categories = db.session.query(ProductCategories)
    next_url, prev_url = paging(products, 'products_list')
    return render_template("products_list.html", products=products.items,
                           categories=categories, next_url=next_url, prev_url=prev_url)


@app.route('/admin/edit_product/<string:product_id>', methods=("GET", "POST"))
@login_required
def edit_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    form = AddProductForm()
    form.category_id.choices = [(int(category.id), category.name) for category in ProductCategories.query.all()]
    if request.method == "POST" and form.validate():
        try:
            form.populate_obj(product)
            db.session.commit()
            flash("Product edited")
            if form.image.data:
                remove_images(f'{product_id}.jpg', f'{product_id}_thumbnail.jpg')
                save_image_and_thumbnail(form.image.data, product.id)
        except IntegrityError:
            flash('Product was not edited!!')
        return redirect(url_for('products_list'))
    elif request.method == "GET":
        form = AddProductForm(formdata=request.form, obj=product)
        form.category_id.choices = [(int(category.id), category.name) for category in ProductCategories.query.all()]
        form.category_id.default = (product.category_id, product.category.name)
    return render_template("edit_product.html", form=form, product_id=product.id)


@app.route('/admin/delete_news/<string:news_id>', methods=("GET", "POST"))
@login_required
def delete_news_id(news_id):
    News.query.filter(News.id == news_id).delete()
    db.session.commit()
    flash('News was successfully deleted from db.')
    return redirect(url_for('news_list'))


@app.route('/admin/news_list', methods=("GET", "POST"))
@login_required
def news_list():
    news = db.session.query(News) \
        .join(Users) \
        .add_columns(News.id, News.title, News.post, News.news_date,
                     Users.first_name, Users.second_name) \
        .filter(Users.id == News.id_user).all()
    return render_template("news_list.html", news=news)


@app.route('/admin/edit_news/<string:news_id>', methods=("GET", "POST"))
@login_required
def edit_news_id(news_id):
    post = News.query.filter(News.id == news_id).first()
    if request.method == 'POST':
        form = NewsForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        flash('News was successfully updated in db.')
        return redirect(url_for('news_list'))
    form = NewsForm(obj=post)
    return render_template('edit_news_id.html', post=post, form=form)


@app.route("/admin/delete_product", methods=("GET", "POST"))
@login_required
def delete_product():
    all_products = products.get_all(g.db)
    return render_template("delete_product.html", products=all_products)


@app.route("/admin/delete_confirm/<product_id>", methods=("GET", "POST"))
@login_required
def delete_confirm(product_id):
    product = db.session.query(Products).filter_by(id = product_id).first()
    return render_template("delete_confirm.html", product=product)


@app.route("/admin/delete_confirm/delete/<product_id>", methods=("GET", "POST"))
@login_required
def delete(product_id):
    remove_images(f'{product_id}.jpg', f'{product_id}_thumbnail.jpg')
    Products.query.filter_by(id=product_id).delete()
    db.session.commit()
    return redirect(url_for('products_list'))


def remove_images(*names):
    """Delete image"""
    for name in names:
        img_to_rem = Path(f"app/static/img/{name}")
        if img_to_rem.is_file():
            img_to_rem.unlink()
    return True


@app.route('/admin/categories_list', methods=("GET", "POST"))
@login_required
def categories_list():
    page = request.args.get('page', 1, type=int)
    categories = ProductCategories.query.order_by(ProductCategories.id).paginate(page, ITEMS_PER_PAGE, False)
    next_url, prev_url = paging(categories, 'categories_list')
    return render_template("categories_list.html", categories=categories.items,
                           next_url=next_url, prev_url=prev_url)


@app.context_processor
def inject_email():
    user_email = ''
    if 'user_id' in session:
        user = Users.query.filter_by(id=session['user_id']).first()
        user_email = user.email
    return {'user_email': user_email}


@app.route('/cart/create_order', methods=("GET", "POST"))
@login_required
def create_order():
    new_order = []
    if request.method == "POST":
        all_ids = db.session.query(Cart.id_product).filter(Cart.id_user == session['user_id']).all()
        all_ids = [i[0] for i in all_ids]
        user_order = Orders(id_user=session['user_id'], order_date=datetime.now())
        db.session.add(user_order)
        db.session.commit()
        try:
            send_mail(user_order.users.email, "Ma shop", f"Order #{user_order.id} was created")
        except ConnectionRefusedError as error:
            print(error)
        for product_id in all_ids:
            product_order = OrderProduct(id_order=user_order.id, id_product=product_id)
            db.session.add(product_order)
        Cart.query.filter_by(id_user=session["user_id"]).delete()
        db.session.commit()
    return render_template("create_order.html", new_order=new_order)


@app.route('/admin/manage_orders', methods=("GET", "POST"))
@login_required
def manage_orders():
    all_orders = Orders.query.all()
    return render_template("manage_orders.html", all_orders=all_orders)


@app.route("/set_new_password/<token>", methods=("GET", "POST"))
def set_new_password(token):
    form = SetNewPasswordForm()
    email = False
    try:
        email = confirm_token(token)
    except:
        flash('Link to reset password is invalid or has expired.', 'danger')
    print(email)
    if request.method == "POST":
        new_password = form.password.data
        if email:
            if validation.password_validator(new_password):
                password_hash = generate_password_hash(new_password)
                db.session.query(Users).filter(Users.email == email).update({Users.password: password_hash})
                db.session.commit()
                flash("Your password successfully updated")
                return redirect(url_for("login"))
            else:
                flash("Invalid password")
        else:
            flash("You used invalid link, try again")
    return render_template('set_new_password.html', form=form)


@app.route('/password_recovery', methods=("GET", "POST"))
def password_recovery():
    form = RestorePasswordForm()
    emails_in_db = [item[0] for item in Users.query.with_entities(Users.email).all()]
    print(form.validate())
    print()
    if request.method == "POST":
        email = form.email.data
        token = generate_confirmation_token(email)
        reset_url = app.config["SITE_URL"] + url_for("set_new_password", token=token)
        subject = "Follow this link to reset you password"
        if email in emails_in_db:
            try:
                send_mail(email, subject, reset_url)
                flash('Email with link to restore your password has been sent via email.', 'success')
            except ConnectionRefusedError:
                flash("Cannot connect to the server to send you an email")
        else:
            flash(f"There is no user with email '{email}'")
    return render_template("password_recovery.html", form=form)
