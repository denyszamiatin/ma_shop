from sqlalchemy.exc import IntegrityError

from app.config import basedir, Config
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from flask import request

from app import db, api
from .models import ProductCategories


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

api.add_resource(ProductCategoriesApi, '/api/categories')
api.add_resource(ProductCategoryApi, '/api/category/<uuid>')
