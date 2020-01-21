from sqlalchemy.exc import IntegrityError

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash

from app import db, api
from .models import ProductCategories, Users, Comments, Orders, Products, Cart, OrderProduct
from .models import OrderArchive


class OrderSchema(ModelSchema):
    class Meta:
        model = Orders


order_schema = OrderSchema
orders_schema = OrderSchema(many=True)


class OrdersApi(Resource):
    def get(self):
        orders = Orders.query.all()
        return orders_schema.dump(orders)

    def post(self):
        json_data = request.json
        try:
            order = orders_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        try:
            db.session.add(order)
            db.session.commit()
        except IntegrityError:
            return {"message": "Order exists"}, 409
        return orders_schema.dump(order)


class OrderApi(Resource):
    def get(self, uuid):
        order = Orders.query.filter_by(uuid=uuid).first()
        if not order:
            return {"message": "Order not found"}, 404
        return order_schema.dump(order)

    def put(self, uuid):
        json_data = request.json
        try:
            new_order = order_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        order = Orders.query.filter_by(uuid=uuid).first()
        if not order:
            return {"message": "Order not found"}, 404
        order.name = new_order
        db.session.commit()
        return order_schema.dump(order)

    def delete(self, uuid):
        order = Orders.query.filter_by(uuid=uuid).first()
        if not order:
            return {"message": "Order not found"}, 404
        db.session.delete(order)
        db.session.commit()
        return "", 204


api.add_resource(OrdersApi, '/api/orders')
api.add_resource(OrderApi, '/api/order/<uuid>')


class ProductCategorySchema(ModelSchema):
    class Meta:
        model = ProductCategories

product_category_schema = ProductCategorySchema()
product_categories_schema = ProductCategorySchema(many=True)

class ProductCategoriesApi(Resource):
    def get(self):
        categories = ProductCategories.query.all()
        return product_categories_schema.dump(categories)

    def post(self):
        json_data = request.json
        try:
            category = product_category_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            return {"message": "Category exists"}, 409
        return product_category_schema.dump(category)


class ProductCategoryApi(Resource):
    def get(self, uuid):
        category = ProductCategories.query.filter_by(uuid=uuid).first()
        if not category:
            return {"message": "Category not found"}, 404
        return product_category_schema.dump(category)

    def delete(self, uuid):
        category = ProductCategories.query.filter_by(uuid=uuid).first()
        if not category:
            return {"message": "Category not found"}, 404
        db.session.delete(category)
        db.session.commit()
        return "", 204

    def put(self, uuid):
        json_data = request.json
        try:
            new_category = product_category_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        category = ProductCategories.query.filter_by(uuid=uuid).first()
        if not category:
            return {"message": "Category not found"}, 404
        category.name = new_category.name
        db.session.commit()
        return product_category_schema.dump(category)

api.add_resource(ProductCategoriesApi, '/api/categories')
api.add_resource(ProductCategoryApi, '/api/category/<uuid>')


class UserSchema(ModelSchema):
    class Meta:
        model = Users


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UsersApi(Resource):
    def post(self):
        json_data = request.json
        try:
            user = user_schema.load(json_data, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 422
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {"message": "User already exists"}, 409
        return user_schema.dump(user)

    def get(self):
        users = Users.query.all()
        return users_schema.dump(users)

    def delete(self):
        db.session.query(Users).delete()
        db.session.commit()
        return "", 204


class UserApi(Resource):
    def get(self, uuid):
        user = Users.query.filter_by(uuid=uuid).first()
        if not user:
            return {"massage": "User not found"}, 404
        return user_schema.dump(user)

    def delete(self, uuid):
        user = Users.query.filter_by(uuid=uuid).first()
        if not user:
            return {"massage": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return "", 204

    def put(self, uuid):
        json_data = request.json
        user = Users.query.filter_by(uuid=uuid).first()
        if not user:
            return {"massage": "User not found"}, 404
        try:
            updated_user = user_schema.load(json_data, session=db.session)
            user.first_name = updated_user.first_name
            user.second_name = updated_user.second_name
            user.password = generate_password_hash(updated_user.password)
            db.session.commit()
        except ValidationError as e:
            return {"message": str(e)}, 422
        return user_schema.dump(user)


api.add_resource(UsersApi, '/user')
api.add_resource(UserApi, '/user/<uuid>')


class CommentSchema(ModelSchema):
    class Meta:
        model = Comments


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class CommentsApi(Resource):
    def post(self):
        json_data = request.json
        try:
            comment = comment_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        try:
            db.session.add(comment)
            db.session.commit()
        except IntegrityError:
            return {"message": "Category exists"}, 409
        return comment_schema.dump(comment)

    def get(self):
        comments = Comments.query.all()
        return comments_schema.dump(comments)


class CommentApi(Resource):
    def get(self, id):
        comment = Comments.filter_by(id=id).first()
        if not comment:
            return {"message": "Comment not found"}, 404
        return comment_schema.dump(comment)

    def delete(self, id):
        comment = Comments.filter_by(id=id).first()
        if not comment:
            return {"message": "Comment not found"}, 404
        db.session.delete(comment)
        db.session.commit()
        return "", 204

    def put(self, id):
        json_data = request.json
        comment = Comments.filter_by(id=id).first()
        if not comment:
            return {"message": "Comment not found"}, 404
        comment.body = json_data['body']
        db.session.commit()
        return comment_schema.dump(comment)


api.add_resource(CommentsApi, '/api/comment')
api.add_resource(CommentApi, '/api/comment/<id>')


class OrderArchiveSchema(ModelSchema):
    class Meta:
        model = OrderArchive


order_archive_schema = OrderArchiveSchema()
orders_archive_schema = OrderArchiveSchema(many=True)


class OrdersArchiveApi(Resource):
    def get(self):
        orders_archive = OrderArchive.query.all()
        return orders_archive_schema.dump(orders_archive)

    def post(self):
        json_data = request.json
        try:
            order_archive = orders_archive_schema.load(json_data, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 422
        try:
            db.session.add(order_archive)
            db.session.commit()
        except IntegrityError:
            return {'message': 'Order is already in Archive'}, 409
        return orders_archive_schema.dump(order_archive)

    def delete(self):
        db.session.query(OrderArchive).delete()
        db.session.commit()
        return "", 204


class OrderArchiveApi(Resource):
    def get(self, uuid):
        order_archive = OrderArchive.query.filter_by(uuid=uuid).first()
        if not order_archive:
            return {'message': 'No such Order in Archive'}, 404
        return order_archive_schema.dump(order_archive)

    def delete(self, uuid):
        order_archive = OrderArchive.query.filter_by(uuid=uuid).first()
        if not order_archive:
            return {"massage": "No such Order in Archive"}, 404
        db.session.delete(order_archive)
        db.session.commit()
        return "", 204


api.add_resource(OrdersArchiveApi, '/api/order_archive')
api.add_resource(OrderArchiveApi, '/api/order_archive/<id>')


class ProductSchema(ModelSchema):
    class Meta:
        model = Products


class ProductsSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Decimal()
    description = fields.String()
    category_id = fields.Nested(ProductCategorySchema)
    deleted = fields.Boolean()


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class ProductsApi(Resource):
    def post(self):
        json_data = request.json
        try:
            product = product_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            return {"message": "Category exists"}, 409
        return product_schema.dump(product)

    def get(self):
        products = Products.query.all()
        return products_schema.dump(products)


class ProductApi(Resource):
    def get(self, id):
        product = Products.filter_by(id=id).first()
        if not product:
            return {"message": "Comment not found"}, 404
        db.session.delete(product)
        db.session.commit()
        return "", 204

    def put(self, id):
        json_data = request.json
        product = Products.filter_by(id=id).first()
        if not product:
            return {"message": "Comment not found"}, 404
        product.name = json_data['name']
        product.price = json_data['price']
        product.description = json_data['description']
        product.category_id = json_data['category_id']
        product.deleted = json_data['deleted']
        db.session.commit()
        return product_schema.dump(product)


api.add_resource(ProductsApi, '/api/product')
api.add_resource(ProductApi, '/api/product/<id>')


class CartSchema(ModelSchema):
    class Meta:
        model = Cart
        include_fk = True


cart_schema = CartSchema()
carts_schema = CartSchema(many=True)


class CartsApi(Resource):
    def post(self):
        """Add new items to the cart"""
        json_data = request.json
        try:
            cart = cart_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        db.session.add(cart)
        db.session.commit()
        return cart_schema.dump(cart)

    def get(self):
        """Return all cart items"""
        cart_items = Cart.query.all()
        return carts_schema.dump(cart_items)


class CartApi(Resource):
    def get(self, ucid):
        """Return all products that user with id 'ucid' has in his cart"""
        cart_items = Cart.query.filter_by(id_user=ucid).all()
        if not cart_items:
            return {"message": "There are no products in the cart"}, 404
        return carts_schema.dump(cart_items)

    def delete(self, ucid):
        """Delete cart item by given 'ucid'"""
        cart_item = Cart.query.filter_by(ucid=ucid).first()
        if not cart_item:
            return {"message": "Product not found"}, 404
        db.session.delete(cart_item)
        db.session.commit()
        return "", 204

    def put(self, ucid):
        """Update id_product value of a Cart object"""
        json_data = request.json
        try:
            new_product_id = json_data['id_product']
        except KeyError:
            return {"message": "New product id expected"}
        cart = Cart.query.filter_by(ucid=ucid).first()
        if not cart:
            return {"message": "Cart not found"}, 404
        cart.id_product = new_product_id
        db.session.commit()
        return cart_schema.dump(cart)


api.add_resource(CartsApi, '/api/cart')
api.add_resource(CartApi, '/api/cart/<ucid>')


class OrderProductSchema(ModelSchema):
    class Meta:
        model = OrderProduct


order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)


class OrderProductsApi(Resource):
    def post(self):
        json_data = request.json
        try:
            order_products = order_products_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        try:
            db.session.add(order_products)
            db.session.commit()
        except IntegrityError:
            return {"message": "Order exists"}, 409
        return order_products_schema.dump(order_products)

    def get(self):
        order_products = OrderProduct.query.all()
        return order_products_schema.dump(order_products)


class OrderProductApi(Resource):
    def get(self, id):
        order_product = OrderProduct.query.filter_by(id_order=id).first()
        if not order_product:
            return {"message": "Order not found"}, 404
        return order_product_schema.dump(order_product)

    def put(self, id):
        json_data = request.json
        try:
            new_order_product = order_product_schema.load(json_data, session=db.session)
        except ValidationError as error:
            return {"message": str(error)}, 422
        order_product = OrderProduct.query.filter_by(id_order=id).first()
        if not order_product:
            return {"message": "Order not found"}, 404
        order_product.name = new_order_product
        db.session.commit()
        return order_schema.dump(order_product)

    def delete(self, id):
        order_product = OrderProduct.query.filter_by(id_order=id).first()
        if not order_product:
            return {"message": "Order not found"}, 404
        db.session.delete(order_product)
        db.session.commit()
        return "", 204


api.add_resource(OrderProductsApi, '/api/order_products')
api.add_resource(OrderProductApi, '/api/order_product/<id>')
