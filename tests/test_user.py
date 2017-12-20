from flask import json,jsonify
from tests import ShoppingListApiTest
class ShoppingApiUserTest(ShoppingListApiTest): 

    def test_addnewuser(self):
        """Test API can create add a new user"""
        self.assertIn("User created",str(self.rs.data))
        self.assertEqual(self.rs.status_code,200)
        l=json.loads(self.rs.data)
        self.assertEqual("User created",l["message"])
        
    def test_if_app_denies_creation_of_users_with_the_same_info(self):
        """Test API can create add a new user"""
        self.rs=self.client.post('/auth/register/',data=self.conevertInfo, content_type='application/json') 
        self.assertIn("User exists",str(self.rs.data))
        self.assertEqual(self.rs.status_code,200)

    def test_LoginUser(self):
        """Test API can login a user"""
        self.assertEqual(self.rsu.status_code,200)
        self.assertIn("dkam6",str(self.rsu.data))

    def test_app_can_logout_user(self):
        """Test API can logout a user"""
        logout=self.client.post('/auth/logout/',
                                headers={
                                    'Content-Type':'application/json',
                                    'x-access-token':self.tok
                                    })
        self.assertIn("You are logout",str(logout.data)) 
        self.assertEqual(logout.status_code,200)
       
    def test_app_can_reset_password(self):
        """Test API can reset a password user"""
        restUserPassword = {'Newpassword':123,"Username":"dkam6","pass":"pass"}
        self.josnrestUserPassword = json.dumps(restUserPassword )
        rest_password=self.client.put('/auth/RestPassword/',
                                    data=self.josnrestUserPassword,
                                    headers={
                                        'Content-Type':'application/json',
                                        'x-access-token':self.tok})
        self.assertEqual(rest_password.status_code,200)