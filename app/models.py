from werkzeug.security import generate_password_hash
from datetime import datetime
from . import db


class OrderArchive(db.Model):
    __tablename__ = "order_archive"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Numeric)
    date_archive = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'<User {self.id}>'


class ProductCategories(db.Model):
    """
    Class to create table "product_categories" in database.
    Variables
    ----------
    id - category id
    name - category name
    products - products relationship
    """
    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    products = db.relationship("Products")

    def __str__(self):
        return self.name


class Cart(db.Model):
    """
    Class to create table "cart" in database.
    Variables
    ----------
    id - cart id
    id_user - ForeignKey users.id
    id_product - ForeignKey products.id
    addition_date - cart create date
    user - users relationship
    product - products relationship
    """
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    addition_date = db.Column(db.Date, default=datetime.today().date())
    user = db.relationship("Users")
    product = db.relationship("Products")

    def __str__(self):
        return f"cart {self.id}"


class News(db.Model):
    """
    Class to create table "news" in database.
    Variables
    ----------
    id
    title
    post
    id_user
    news_date
    Methods
    -------
    __str__
    """
    __tablename__= "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    post = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_date = db.Column(db.Date, default=datetime.utcnow())

    def __str__(self):
        return f'id: {self.id}, user id: {self.id_user} on date:' \
               f' {self.news_dta}, title: {self.title}and all post:{self.post} '


class Mark (db.Model):
    """
    Class to create table "marks" in database.
    Variables
    ----------
    id
    id_user
    id_product
    mark_date
    rating
    users_who_marked
    products_marked

    Methods
    -------
    __str__
    """
    __tablename__ = "marks"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    mark_date = db.Column(db.Date, default=datetime.today().date())
    rating = db.Column(db.Integer)
    users_who_marked = db.relationship("Users")
    products_marked = db.relationship("Products")

    def __str__(self):
        return f'<Mark id {self.id} is rating {self.rating} provided ' \
               f'for product {self.id_product} by user {self.id_user} on {self.mark_date}>'


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_date = db.Column(db.Date, default=datetime.today().date())
    body = db.Column(db.Text)


class Users(db.Model):
    """
    Class to create table "users" in database.
    Variables
    ----------
    id
    first_name
    second_name
    email
    password

    Methods
    -------
    __repr__
    __str__
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(500), nullable=False)
    second_name = db.Column(db.String(500))
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<User id: {self.id}>"

    def __str__(self):
        return f"<User id: {self.id}>"

    def __init__(self, first_name, second_name, email, password):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = generate_password_hash(password)

class Products(db.Model):
    """
    Class to create products table in database.
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    price = db.Column(db.Numeric)
    image = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    deleted = db.Column(db.Boolean, default=False)
    added_to_cart = db.relationship("Cart")
    ordered = db.relationship("OrderProduct")
    marked = db.relationship("Mark")

    def __str__(self):
        return f"<Id: {self.id}, name: {self.name}, price: {self.price}>"


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
