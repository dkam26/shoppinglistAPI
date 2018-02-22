from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import psycopg2, os
from flask_cors import CORS
db_url='postgresql://postgres:masiko26@localhost/shoppinglist'

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='Random key'
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db=SQLAlchemy(app)
api = Api(app)
from my_app import views
db.create_all()
