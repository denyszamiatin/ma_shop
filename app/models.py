from datetime import datetime
from . import db


class OrderArchive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Float)
    date_archive = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class ProductCategories(db.Model):
    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    products = db.relationship("products")


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    addition_date = db.Column(db.Date, default=datetime.today().date())
    user = db.relationship("users")
    product = db.relationship("products")


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(350))
    post = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    news_date = db.Column(db.Date, default=datetime.utcnow())


class Mark (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    mark_date = db.Column(db.Date, default=datetime.today().date())
    rating = db.Column(db.Integer)
    users_who_marked = db.relationship("Users")
    products_marked = db.relationship("Product")


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_date = db.Column(db.Date, default=datetime.today().date())
    body = db.Column(db.Text)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User id: {self.id}>"


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    price = db.Column(db.Float)
    image = db.Column(db.LargeBinary)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    deleted = db.Column(db.Boolean, default=False)


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
