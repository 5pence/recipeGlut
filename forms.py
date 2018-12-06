from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    email = StringField('Email Address', validators=[Length(min=6, max=35), Email()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')


class CreateRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (one per line please)', validators=[DataRequired()])
    method = TextAreaField('Instructions', validators=[DataRequired()])
    tags = StringField('Tags (separate by comma please)', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')


class EditRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (one per line please)', validators=[DataRequired()])
    method = TextAreaField('Instructions', validators=[DataRequired()])
    tags = StringField('Tags (separate by comma please)', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Update Recipe')


class ConfirmDelete(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete this Recipe')