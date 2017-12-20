from flask import json,jsonify
from tests import ShoppingListApiTest
class ShoppinglistItem(ShoppingListApiTest):
    
    def test_app_returns_shoppinglist_items(self):
        """Test API can return a list items """
        product_to_add={'product':'nikes','Quantity':3,'Amountspent':5000}
        jsonproduct_to_add=json.dumps(product_to_add)
        add_list=self.client.post('/shoppinglists/', 
                                    data=self.shopllist, 
                                    headers={
                                        'Content-Type':'application/json',
                                        'x-access-token':self.tok})
        add_product=self.client.post('/shoppinglist/shoes/items/',
                                        data=jsonproduct_to_add,
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        list_of_items=self.client.get('/shoppinglist/shoes/?each_page=1&page_number=1',
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        self.assertIn("Products",str(list_of_items.data)) 
        self.assertEqual(list_of_items.status_code,200)

    def test_app_can_delete_an_item(self):
        """Test API can delete  a item """
        delete_item=self.client.delete('/shoppinglist/shoes/items/nikes',
                                            headers={
                                                'Content-Type':'application/json',
                                                'x-access-token':self.tok})
        self.assertEqual(delete_item.status_code,200)
    
    def tes_app_can_add_and_update_items_in_a_shoppinglist(self):
        """Test API can add and update  an item """
        product_to_add={'product':'nikes','Quantity':3,'Amountspent':5000}
        list_to_be_updated={'Quantity':4,'AmountSpent':4500}
        self.jsonproduct_to_add=json.dumps(product_to_add)
        self.jsonlist_to_be_updated=json.dumps(list_to_be_updated)
        add_list=self.client.post('/shoppinglists/', 
                                    data=self.shopllist, 
                                    headers={
                                        'Content-Type':'application/json',
                                        'x-access-token':self.tok})
        add_product=self.client.post('/shoppinglist/shoes/items/',
                                        data=self.jsonproduct_to_add,
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        update_product=self.client.put('/shoppinglist/shoes/items/nikes',
                                        data=self.jsonlist_to_be_updated,
                                        headers={
                                            'Content-Type':'application/json',
                                            'x-access-token':self.tok})
        self.assertEqual(add_product.status_code,200)
        self.assertEqual(update_product.status_code,200)
        