from decimal import Decimal
import datetime
from my_app import db
class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    Surname = db.Column(db.String(255))
    Firstname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
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
    shoppinglist_name=db.Column(db.String(255),unique=True)
    user=db.Column(db.String(255))
    products=db.relationship("Product",backref="Shoppinglists")
    def __init__(self,shoppinglist_name,user):
        self.shoppinglist_name=shoppinglist_name
        self.user=user
    def __repr__(self):
        return '<Shoppinglists %d>'% self.id
class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer,primary_key=True)
    product = db.Column(db.String(255),unique=True)
    Quantity = db.Column(db.Integer)
    AmountSpent = db.Column(db.Integer)
    shoppinglist=db.Column(db.String(255))
    shoppinglist_id=db.Column(db.Integer,db.ForeignKey("Shoppinglists.id"))
    def __init__(self ,product ,Quantity ,AmountSpent, shoppinglist_id):
        self.product = product
        self.shoppinglist = shoppinglist_id
        self.Quantity = Quantity
        self.AmountSpent = AmountSpent
    def __repr__(self):
        return '<Product %d>'% self.id
class Store():
    def register(self,newadd):
        db.session.add(newadd)
        db.session.commit()
    def edit(self,newedit):
        db.session.delete(newedit)
        db.session.commit()





