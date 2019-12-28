from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DecimalField, TextAreaField, FileField, SelectField, PasswordField
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
    title = StringField("Title")
    post = TextAreaField("Post")


class UserRegistrationForm(FlaskForm):
    first_name = StringField("First name",  validators=[DataRequired()])
    second_name = StringField("Second name",  validators=[DataRequired()])
    email = StringField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
