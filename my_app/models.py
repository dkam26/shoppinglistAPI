from my_app import db
import datetime
from flask_wtf import Form
from wtforms import TextField,DecimalField,PasswordField
from wtforms.validators import InputRequired,NumberRange
from decimal import Decimal

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    Surname = db.Column(db.String(255))
    Firstname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Shoppinglists = db.relationship('Shoppinglists', backref='user')
    def __init__(self, user, Surname, Firstname, email, Password):
        self.user = user
        self.Surname = Surname
        self.Firstname = Firstname
        self.email = email
        self.Password = Password
    def __repr__(self):
        return '<User %d>'% self.id

class Shoppinglists(db.Model):
    __tablename__="Shoppinglists"
    id= db.Column(db.Integer,primary_key=True)
    sL_id=db.Column(db.Integer,db.ForeignKey('User.id'))
    user_id = db.Column(db.String(255))
    shoppinglist_name=db.Column(db.String(255))
    Product = db.relationship('Product', backref='shoppinglist')
    def __init__(self,user_id,shoppinglist_name):
        self.user_id=user_id
        self.shoppinglist_name=shoppinglist_name
    def __repr__(self):
        return '<Shoppinglists %d>'% self.id


class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer,primary_key=True)
    product = db.Column(db.String(255))
    Quantity = db.Column(db.Integer)
    AmountSpent = db.Column(db.Integer)
    P_id=db.Column(db.Integer,db.ForeignKey('Shoppinglists.id'))
    shoppinglist_id = db.Column(db.String(255))
    def __init__(self ,product ,Quantity ,AmountSpent ,shoppinglist_id):
        self.product = product
        self.shoppinglist_id= shoppinglist_id
        self.Quantity = Quantity
        self.AmountSpent = AmountSpent
    def __repr__(self):
        return '<Product %d>'% self.id

class ProductForm(Form):
    product=TextField('Product', validators=[InputRequired()])
    Quantity=TextField('Quantity', validators=[InputRequired()])
    AmountSpent=DecimalField('Amount spent', validators=[InputRequired(),NumberRange(min=Decimal('0.0'))])
class LoginForm(Form):
    UserName=TextField('UserName', validators=[InputRequired()])
    LoginPassword=PasswordField('Password', validators=[InputRequired()])





