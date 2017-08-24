from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://deo:masiko26@localhost/shoppinglist'
app.config['SECRET_KEY']='Random key'
db=SQLAlchemy(app)
from my_app.views import shoppinglist
app.register_blueprint(shoppinglist)

db.create_all()