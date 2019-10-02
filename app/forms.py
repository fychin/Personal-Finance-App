from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, DecimalField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Email, EqualTo
from app.models import User, Account

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # second password input to prevent typo
    password2 = PasswordField('Confirm password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please try another username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please try another email address.')


class EditAccountForm(FlaskForm):
    id = HiddenField()
    user_id = HiddenField()
    name = StringField('Account Name', validators=[InputRequired()])
    balance = DecimalField('Balance', validators=[InputRequired()])
    submit = SubmitField('Update')

    def __init__(self, original_account_name, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.original_account_name = original_account_name

    def validate_name(self, account_name):
        if account_name.data != self.original_account_name:
            # attempt to find duplicates
            account = Account.query.filter_by(name=self.name.data).first()
            if account is not None:
                raise ValidationError('Account name already exists.')
