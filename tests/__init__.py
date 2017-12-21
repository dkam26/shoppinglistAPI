
from flask import Flask,request,jsonify,session,json
from flask_restful import Resource,Api
import unittest as unittest
from my_app import app,db
from my_app.views import api,AddNewUser,PostUserShoppinglist
from my_app.models import User,Product
import jwt
from functools import wraps
import datetime 

class ShoppingListApiTest(unittest.TestCase):
     
    def setUp(self):
        self.app=app
        self.client=app.test_client()
        self.userInfo={"user":"dkam6", "Surname":"Kamara", "Email":"dkam26@ymail.com", "Firstname":"deo", "Password":"pass"}
        self.user={"user":"dkam6", "Password":"pass"}
        self.shoplist={"newlist":"shoes"}
        self.renamelist={"newName":"underwear"}
        self.shopllist=json.dumps(self.shoplist)
        self.conevertInfo=json.dumps(self.userInfo)
        self.conevertUser=json.dumps(self.user)
        with self.app.app_context():
            db.create_all()
        self.rs=self.client.post('/auth/register/',data=self.conevertInfo, content_type='application/json') 
        self.rsu=self.client.post('/auth/login/', data=self.conevertUser, content_type='application/json')
        tok1=json.loads(self.rsu.data)
        self.tok = tok1['token']

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()