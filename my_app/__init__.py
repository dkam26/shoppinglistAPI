from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://deo:masiko26@localhost/shoppinglist'
app.config['SECRET_KEY']='Random key'
db=SQLAlchemy(app)


db.create_all()