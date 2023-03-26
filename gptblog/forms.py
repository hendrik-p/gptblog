from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Content', validators=[DataRequired()])
    teaser = StringField('Teaser', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
