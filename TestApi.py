import os
from my_app import app,db
from my_app.models.models import User,Product,Store
from flask import Flask,request,jsonify,session
from flask_restful import Resource,Api
import unittest2 as unittest2
from my_app import db,app
from Api import api,AddNewUser,postUserShoppinglist
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from functools import wraps
import datetime 
import json
store=Store()
class ShoppingListApiTest(unittest2.TestCase): 
    def setUp(self):
        self.app=app
        self.client=self.app.test_client
        self.userInfo={"user":"dkam26","Surname":"Kamara","Email":"dk@ymail.com","Firstname":"deo","Password":"pass"}
        self.user={"user":"dkam26","Password":"pass"}
        self.shoplist={"newlist":"shoes"}
        self.shopllist=json.dumps(self.shoplist)
        self.conevertInfo=json.dumps(self.userInfo)
        self.conevertUser=json.dumps(self.user)
        with self.app.app_context():
            db.create_all()
    def test_addnewuser(self):
        rs=self.client().post('/auth/register/',data=self.conevertInfo, content_type='application/json') 
        self.assertIn("User created",str(rs.data))
        self.assertEqual(rs.status_code,200)
    def test_LoginUser(self):
        rs=self.client().post('/auth/register/',data=self.conevertInfo, content_type='application/json') 
        self.assertEqual(rs.status_code,200)
        rs=self.client().post('/auth/login/',data=self.conevertUser,content_type='application/json') 
        self.assertEqual(rs.status_code,200)
        self.assertIn("dkam26",str(rs.data))
    

    def tearDown(self):
        
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    

        
if __name__=='__main__':
    unittest2.main()


  