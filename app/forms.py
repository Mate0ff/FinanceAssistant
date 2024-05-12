from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError, NumberRange
from wtforms_components import DateRange
from app.models import User
from decimal import Decimal
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    gender = SelectField('Gender', choices=['Male','Female'])
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()  
        if user:
            raise ValidationError('That username is taken. Choose different one!')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()  
        if user:       
            raise ValidationError('There is already account with that email!')
    

class LoginForm(FlaskForm):
    
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class LimitForm(FlaskForm):
    needs = IntegerField('Needs',validators=[DataRequired()])
    wants = IntegerField('Wants',validators=[DataRequired()])
    other = IntegerField('Other',validators=[DataRequired()])

    submit = SubmitField('Accept')

class CreateIncomeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=25)])
    category = SelectField('Category', choices=['Salary','Bonus','Gift','Rent','Scholarship','Investment','Other'])
    date = DateField('Date')
    amount = DecimalField('Amount',places=2, validators=[DataRequired(),NumberRange(min=0.01)])
    note = TextAreaField('Note', validators=[DataRequired(), Length(min=2,max=45)])

    submit = SubmitField('Create')

    def validate_amount(form, field):
        try:
            amount = Decimal(field.data)
            if amount % Decimal('0.01') != 0:
                raise ValidationError('Amount must have at most 2 decimal places')
        except:
            raise ValidationError('Invalid amount format')


class CreateExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=25)])
    category = SelectField('Category', choices=['Home','Transport','Education','Food','Healthcare','Entertainment','Debt','Clothes','Travel','Investment','Other'])
    type = SelectField('Type', choices=['Needs','Wants','Other'])
    date = DateField('Date')
    amount = DecimalField('Amount',places=2, validators=[DataRequired(),NumberRange(min=0.01)])
    note = TextAreaField('Note', validators=[DataRequired(), Length(min=2,max=45)])

    submit = SubmitField('Create')

    def validate_amount(form, field):
        try:
            amount = Decimal(field.data)
            if amount % Decimal('0.01') != 0:
                raise ValidationError('Amount must have at most 2 decimal places')
        except:
            raise ValidationError('Invalid amount format')
    
class DatePickerForm(FlaskForm):
    date = DateField('Date',id='date-picker')

class PdfDatePickerForm(FlaskForm):
    from_date = DateField('From', validators=[DateRange(max=date.today())])
    to_date = DateField('To', validators=[DateRange(max=date.today())])
    submit = SubmitField('Create')

    def validate_to_date(self, to_date):
        if to_date.data <= self.from_date.data:
            raise ValidationError("The 'To' date must be later than the 'From' date.")