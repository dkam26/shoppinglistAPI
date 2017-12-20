from flask import json,jsonify
from tests import ShoppingListApiTest
class Shoppinglist(ShoppingListApiTest):

    def test_if_app_gets_shoppinglists(self):
        """Test API can get a user shopppinglist"""
        li = self.client.get('/shoppinglists/?each_page=1&page_number=1',
                            headers = {
                                'Content-Type':'application/json',
                                'x-access-token':self.tok})
        self.assertEqual(li.status_code, 200)

    def test_if_app_can_search_for_existing_lists_with_products(self):
        """Test API can search for a list and its products"""
        product_to_add = {'product':'nikes', 'Quantity':3, 'Amountspent':5000}
        jsonproduct_to_add = json.dumps(product_to_add)
        add_list = self.client.post('/shoppinglists/',
                                     data = self.shopllist, 
                                     headers = {
                                         'Content-Type':'application/json',
                                         'x-access-token':self.tok})
        add_product=self.client.post('/shoppinglist/shoes/items/',
                                        data=jsonproduct_to_add,
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        searchforlists=self.client.get('/search/?q=shoes',
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        searchforproducts=self.client.get('/searchProduct/?q=nike',
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        self.assertIn("existing products of searched list",str(searchforlists.data))
        self.assertIn("Searched product",str(searchforproducts.data))
        self.assertEqual(searchforproducts.status_code,200)
        self.assertEqual(searchforlists.status_code,200) 
    
    def test_if_app_can_search_for_existing_list_without_products(self):
        """Test API can search for a list with no products"""
        add_list=self.client.post('/shoppinglists/', 
                                    data=self.shopllist,
                                    headers={
                                        'Content-Type':'application/json',
                                        'x-access-token':self.tok})
        searchforlists=self.client.get('/search/?q=shoes',
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        self.assertEqual(searchforlists.status_code,200) 
        self.assertIn("shoes Shoppinglist still empty",str(searchforlists.data)) 

    def test_app_can_update_a_list(self):
        """Test API can update  a list """
        self.ne=json.dumps({"newName":"pants"})
        list_update=self.client.put('/shoppinglists/trou',
                                    data=self.ne,
                                    headers={
                                        'Content-Type':'application/json',
                                        'x-access-token':self.tok})
        self.assertIn("list doesnt exist",str(list_update.data)) 
        self.assertEqual(list_update.status_code,200)

    def test_app_can_add_list(self):
        """Test API can add  a product in a  list """
        add_list=self.client.post('/shoppinglists/', 
                                data=self.shopllist, 
                                headers={
                                    'Content-Type':'application/json',
                                    'x-access-token':self.tok})
        self.assertEqual(add_list.status_code,200)
    
    def test_app_can_delete_list(self):
        """Test API can delete a list """
        delete_list=self.client.delete('/shoppinglists/nikes',
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        self.assertEqual(delete_list.status_code,200)