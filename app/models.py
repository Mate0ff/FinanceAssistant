from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0)
    wants = db.Column(db.Integer, nullable=False, default=1000)
    needs = db.Column(db.Integer, nullable=False, default=1000)
    other = db.Column(db.Integer, nullable=False, default=1000)
    
    incomes = db.relationship('Income', backref='user')
    expenses = db.relationship('Expense', backref='user')

class IncomeCategory(db.Model):
    __tablename__ = 'income_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    icon = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    incomes = db.relationship('Income', backref='category')

class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    icon = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    expenses = db.relationship('Expense', backref='category')

class ExpenseType(db.Model):
    __tablename__ = 'expense_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    expenses = db.relationship('Expense', backref='expense_type')

class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('income_categories.id'))
    name = db.Column(db.String(25),unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(40), nullable=False, default='')

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('expense_types.id'))
    name = db.Column(db.String(25),unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(40), nullable=False, default='')

