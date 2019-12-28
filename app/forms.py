from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DecimalField, TextAreaField, FileField, SelectField, PasswordField, \
    IntegerField
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


class UserRegistrationForm(FlaskForm):
    """User registration form"""
    first_name = StringField("First name",  validators=[DataRequired()])
    second_name = StringField("Second name",  validators=[DataRequired()])
    email = StringField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserLoginForm(FlaskForm):
    """User login form"""
    email = StringField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
