from decimal import Decimal
import datetime
from my_app import db

class User(db.Model):
    """Table for users"""
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    Surname = db.Column(db.String(255))
    Firstname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    def __init__(self,user, Surname, Firstname ,email,Password):
        self.username=user
        self.Surname=Surname
        self.Firstname= Firstname 
        self.email=email
        self.Password=Password
    def __repr__(self):
        return '<User %d>'% self.id

class Shoppinglists(db.Model):
    """Table for shoppinglists created by users"""
    __tablename__="Shoppinglists"
    id= db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("User.id"))
    shoppinglist_name=db.Column(db.String(255), unique=True)
    user=db.Column(db.String(255))
    products=db.relationship("Product",backref="Shoppinglist", lazy='dynamic', cascade="all, delete-orphan")
    def __init__(self,shoppinglist,user):
        self.shoppinglist_name=shoppinglist
        self.user=user

    def register(self,newadd):
        db.session.add(newadd)
        db.session.commit()
    def edit(self,newedit):
        db.session.delete(newedit)
        db.session.commit()
    def __repr__(self):
        return '<Shoppinglists %d>'% self.id

class Product(db.Model):
    """Table for products under  shoppinglists created by users"""
    __tablename__ = "Product"
    id = db.Column(db.Integer,primary_key=True)
    shoppinglist_id=db.Column(db.Integer,db.ForeignKey("Shoppinglists.id"))
    shoppinglist = db.Column(db.String(255))
    product = db.Column(db.String(255))
    Quantity = db.Column(db.Integer)
    AmountSpent = db.Column(db.Integer)
    def __init__(self, quantity, amountspent, shoppinglist_id,product):
        self.shoppinglist=shoppinglist_id
        self.product = product
        self.Quantity = quantity
        self.AmountSpent = amountspent
    def register(self,newadd):
        db.session.add(newadd)
        db.session.commit()
    def edit(self,newedit):
        db.session.delete(newedit)
        db.session.commit()
    def __repr__(self):
        return '<Product %d>'% self.id
