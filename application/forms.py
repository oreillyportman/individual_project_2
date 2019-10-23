from flask_wtf import FlaskForm, Form
from flask_login import current_user
from wtforms import Form, StringField, SelectField, validators, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users

class RegistrationForm(FlaskForm):
  first_name = StringField('First Name',
    validators=[
      DataRequired(),
      Length(min=4, max=30)
    ])
  last_name = StringField('Last Name',
    validators=[
      DataRequired(),
      Length(min=4, max=30)
    ])
  email = StringField('Email',
    validators=[
      DataRequired(),
      Email()
    ])
  password = PasswordField('Password',
    validators=[
      DataRequired()
    ])  
  confirm_password = PasswordField('Conform Password',
    validators=[
      DataRequired(),
      EqualTo('password')
    ])
  submit = SubmitField('Sign Up')

  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
  email = StringField('Email',
    validators=[
      DataRequired(),
      Email()
    ])
  password = PasswordField('Password',
    validators=[
      DataRequired()
    ])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
  first_name = StringField('First Name',
    validators=[
      DataRequired(),
      Length(min=4, max=30)
    ])
  last_name = StringField('Last Name',
    validators=[
      DataRequired(),
      Length(min=4, max=30)
    ])
  email = StringField('Email',
    validators=[
      DataRequired(),
      Email()
    ])
  submit = SubmitField('Update Account Details!')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = Users.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Email already in use - Please choose another!')
'''--------------------------------------'''
class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

class AlbumForm(Form):
    media_types = [('Digital', 'Digital'),
                   ('CD', 'CD'),
                   ('Cassette Tape', 'Cassette Tape')
                   ]
    artist = StringField('Artist')
    title = StringField('Title')
    release_date = StringField('Release Date')
    publisher = StringField('Publisher')
    media_type = SelectField('Media', choices=media_types)

class AlbumEditForm(Form):
    media_types = [('Digital', 'Digital'),
                   ('CD', 'CD'),
                   ('Cassette Tape', 'Cassette Tape')
                   ]
    actions = [('Update', 'Update'),('Delete','Delete')]
    artist = StringField('Artist')
    title = StringField('Title')
    release_date = StringField('Release Date')
    publisher = StringField('Publisher')
    media_type = SelectField('Media', choices=media_types)
    action = SelectField('Action', choices=actions)
