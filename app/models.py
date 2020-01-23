import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import app
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
    uuid = db.Column(db.String(36), unique=True)
    products = db.relationship("Products", cascade="delete", backref="category", lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.uuid = str(uuid.uuid4())

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
    addition_date = db.Column(db.Date, default=datetime.utcnow())
    ucid = db.Column(db.String(36), unique=True)
    users = db.relationship("Users")
    product = db.relationship("Products")

    def __init__(self, id_user, id_product):
        self.ucid = str(uuid.uuid4())
        self.id_user = id_user
        self.id_product = id_product

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
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    post = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_date = db.Column(db.Date, default=datetime.utcnow())

    def __str__(self):
        return f'id: {self.id}, user id: {self.id_user} on date:' \
               f' {self.news_dta}, title: {self.title}and all post:{self.post} '


class Mark(db.Model):
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

    def __init__(self, id_user, id_product, rating):
        self.id_user = id_user
        self.id_product = id_product
        self.rating = rating

    def __str__(self):
        return f'<Mark id {self.id} is rating {self.rating} provided ' \
               f'for product {self.id_product} by user {self.id_user} on {self.mark_date}>'


class Comments(db.Model):
    """
        Class to create table "comments" in database.
        Variables
        ----------
        id
        body
        comment_date
        id_product
        id_user
        uuid_user
        Methods
        -------
        __repr__
        """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    comment_date = db.Column(db.Date, default=datetime.today().date())
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Comment id <{self.id}>: '<{self.body}>' provided for product {self.id_product} " \
               f"by user {self.id_user} on {self.comment_date}"


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
    uuid = db.Column(db.String(36), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    admin_role = db.Column(db.Boolean())
    comments = db.relationship("Comments")

    def __init__(self, first_name, second_name, email, password, admin_role, confirmed):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = generate_password_hash(password)
        self.uuid = str(uuid.uuid4())
        self.admin_role = admin_role
        self.confirmed = confirmed

    def __repr__(self):
        return f"<User id: {self.id}>"

    def __str__(self):
        return f"<User id: {self.id}>"


class Products(db.Model):
    """
    Class to create products table in database.
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(app.config['PRODUCT_NAME_MAX_LENGTH']))
    price = db.Column(db.Numeric)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    deleted = db.Column(db.Boolean, default=False)
    added_to_cart = db.relationship("Cart")
    ordered = db.relationship("OrderProduct")
    marked = db.relationship("Mark")
    commented = db.relationship("Comments")

    def __str__(self):
        return f"<Id: {self.id}, name: {self.name}, price: {self.price}>"


class OrderProduct(db.Model):
    """
    Class to create table "order_product" in database.
    Variables
    ----------
    id - order_product id
    name - order id
    products - product id
    """
    id = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    orders = db.relationship('Orders')
    products = db.relationship('Products')

    def __init__(self, id_order, id_product):
        self.id_order = id_order
        self.id_product = id_product

    def __repr__(self):
        return f'<Order_id: {self.id_order}, product_id: {self.id_product}>'

    def __str__(self):
        return f'<Order_id: {self.id_order}, product_id: {self.id_product}>'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(35), default='New order')
    users = db.relationship('Users')

    def __init__(self, id_user, order_date):
        self.id_user = id_user
        self.order_date = order_date
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'<User_id: {self.id_user}, date: {self.order_date}>'

    def __str__(self):
        return f'<User_id: {self.id_user}, date: {self.order_date}>'
