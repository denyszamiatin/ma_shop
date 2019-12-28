from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DecimalField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    """
    Form to add products.
    """
    name = StringField("Name", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    image = FileField("Image")
    description = TextAreaField("Description", validators=[DataRequired()])
    category_id = SelectField("Category", choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")


class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    post = TextAreaField("Post", validators=[DataRequired()])
    id_user = IntegerField("Id_user", validators=[DataRequired()])
