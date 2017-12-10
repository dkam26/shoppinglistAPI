import os
from my_app import app,db
from my_app.models import User,Product,Store
from flask import Flask,request,jsonify,session
from flask_restful import Resource,Api
import unittest as unittest
from my_app.views import api,AddNewUser,PostUserShoppinglist
import jwt
from functools import wraps
import datetime 
import json
store=Store()
class ShoppingListApiTest(unittest.TestCase): 
    def setUp(self):
        self.app=app
        
        self.client=app.test_client()
        self.userInfo={"user":"dkam6","Surname":"Kamara","Email":"dkam26@ymail.com","Firstname":"deo","Password":"pass"}
        self.user={"user":"dkam6","Password":"pass"}
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

    def test_addnewuser(self):
        self.assertIn("User created",str(self.rs.data))
        self.assertEqual(self.rs.status_code,200)
        l=json.loads(self.rs.data)
        self.assertEqual("User created",l["message"])
    def test_LoginUser(self):
        self.assertEqual(self.rsu.status_code,200)
        self.assertIn("dkam6",str(self.rsu.data))
    def test_if_app_gets_shoppinglists(self):
        li=self.client.get('/shoppinglists/1',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(li.status_code,200)
    def test_if_app_can_search_for_lists(self):
        searchforlists=self.client.get('/searchlist/trousers',headers={'Content-Type':'application/json','x-access-token':self.tok})
        searchforproducts=self.client.get('/searchProduct/khaki',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertIn("existing products of searched list",str(searchforlists.data))   
        self.assertIn("Searched product",str(searchforproducts.data)) 
        self.assertEqual(searchforproducts.status_code,200)
        self.assertEqual(searchforlists.status_code,200)
    def test_app_can_logout_user(self):
        logout=self.client.post('/auth/logout/',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertIn("You are logout",str(logout.data)) 
        self.assertEqual(logout.status_code,200)
       
    def test_app_returns_shoppinglist_items(self):
        list_of_items=self.client.get('/shoppinglist/trousers/1',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertIn("Products",str(list_of_items.data)) 
        self.assertEqual(list_of_items.status_code,200)
    def test_app_can_update_a_list(self):
        self.ne=json.dumps({"newName":"pants"})
        list_update=self.client.put('/shoppinglists/trou',data=self.ne,headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertIn("list doesnt exist",str(list_update.data)) 
        self.assertEqual(list_update.status_code,200)
    def test_app_can_add_list(self):
        add_list=self.client.post('/shoppinglists/', data=self.shopllist, headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(add_list.status_code,200)
    def test_app_can_search_a_product(self):
        search_product=self.client.get('/searchProduct/nikes',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(search_product.status_code,200)
    def test_app_can_delete_list(self):
        delete_list=self.client.delete('/shoppinglists/nikes',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(delete_list.status_code,200)
    def test_app_can_delete_an_item(self):
        delete_item=self.client.delete('/shoppinglist/shoes/items/nikes',headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(delete_item.status_code,200)
    def test_app_can_reset_password(self):
        restUserPassword = {'Newpassword':123,"Username":"dkam6","pass":"pass"}
        self.josnrestUserPassword = json.dumps(restUserPassword )
        rest_password=self.client.put('/auth/RestPassword/',data=self.josnrestUserPassword,headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(rest_password.status_code,200)
    def tes_app_can_add_and_update_items_in_a_shoppinglist(self):
        product_to_add={'product':'nikes','Quantity':3,'Amountspent':5000}
        list_to_be_updated={'Quantity':4,'AmountSpent':4500}
        self.jsonproduct_to_add=json(product_to_add)
        self.jsonlist_to_be_updated=json(list_to_be_updated)
        add_list=self.client.post('/shoppinglists/', data=self.shopllist, headers={'Content-Type':'application/json','x-access-token':self.tok})
        add_product=self.client.post('/shoppinglist/shoes/items/',data=self.jsonproduct_to_add,headers={'Content-Type':'application/json','x-access-token':self.tok})
        update_product=self.client.put('/shoppinglist/shoes/items/nikes',data=self.jsonlist_to_be_updated,headers={'Content-Type':'application/json','x-access-token':self.tok})
        self.assertEqual(add_product.status_code,200)
        self.assertEqual(update_product.status_code,200)
        
    def tearDown(self):
        
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    

        
if __name__=='__main__':
    unittest.main()


  