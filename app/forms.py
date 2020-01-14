from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.fields import StringField, SubmitField, DecimalField, TextAreaField, SelectField, PasswordField, \
    IntegerField, RadioField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField


class AddProductForm(FlaskForm):
    """
    Form to add products.
    """
    name = StringField("Name", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField("Description", validators=[DataRequired()])
    category_id = SelectField("Category", choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")


class NewsForm(FlaskForm):
    """Form for adding news"""
    title = StringField("Title", validators=[DataRequired()])
    post = TextAreaField("Post", validators=[DataRequired()])


class UserRegistrationForm(FlaskForm):
    """User registration form"""
    first_name = StringField("First name",  validators=[DataRequired()])
    second_name = StringField("Second name",  validators=[DataRequired()])
    email = EmailField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserLoginForm(FlaskForm):
    """User login form"""
    email = StringField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CategoryForm(FlaskForm):
    """Form to add category"""
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MarkForm(FlaskForm):
    """Form for product evaluation"""
    mark = RadioField(label='Mark', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    submit = SubmitField("Rate product")


class CommentsForm(FlaskForm):
    """Form for leaving comments"""
    comment = TextAreaField("Leave your comment please", validators=[DataRequired()])
    submit = SubmitField("Add comment")

class RestorePasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class SetNewPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")