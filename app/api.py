from sqlalchemy.exc import IntegrityError

from marshmallow_sqlalchemy import ModelSchema
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash

from app import db, api
from .models import ProductCategories, Users


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


api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/user/<uuid>')