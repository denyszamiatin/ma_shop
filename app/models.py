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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
    addition_date = db.Column(db.Date, default=datetime.today().date())


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(350))
    post = db.Column(db.String(2000))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    news_date = db.Column(db.Date, default=datetime.utcnow())

