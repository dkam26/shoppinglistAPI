from flask import Flask, request, jsonify, session, make_response
from flask_restful import Resource, Api,HTTPException
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email
import jwt, datetime
from my_app.models import User, Product, Shoppinglists
from my_app import db, app
api = Api(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing !'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message':'Token is invalid !'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

class AddNewUser(Resource):
    """API to add user"""
    def post(self):
        data = request.get_json()
        user = data.get('user')
        surname = data.get('Surname')
        email = data.get('Email')
        firstname = data.get('Firstname')
        password = data.get('Password')
        if validate_email(email):
            #To confirm if all the required info is submitted
            if not user or not surname or not email or not firstname or not password:
                return jsonify({"message":"Missing information about the user"})
            else:
                if type(surname) is int or type(firstname) is int:
                    return jsonify({'message':'firstname or surname cant be numbers '})
                else:
                    existing_user = User.query.filter_by(username=user).first()
                    existing_email = User.query.filter_by(email=email).first()
                    if existing_email is None and existing_user is None:
                        #New user to be registered
                        newUser=User(user.lower(), surname.lower(), firstname.lower(),email, password)
                        db.session.add(newUser)
                        db.session.commit()
                        return jsonify({'message':'User created'})
                    else:
                        return jsonify({'message':"User exists"})
        return jsonify({'message':"Invalid email"})

class UserLogin(Resource):
    """User to login"""
    def post(self):
        data = request.get_json()
        user = data.get('user')
        password = data.get('Password')
        #To confirm if all the required info is submitted
        if not data or not password:
            return jsonify({"message":"Missing information about the user"})
        else:
            users = User.query.filter_by(username=user, Password=password).first()
            #confirm the User is registered
            if users:
                session['loggedUser'] = users.username
                token = jwt.encode({
                'id':users.id,
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
                }, app.config['SECRET_KEY'])
                return jsonify({'Welcome':session['loggedUser'] , 'token':token.decode('UTF-8')})
            return jsonify({'message':'Wrong creditinals'})

class Search(Resource):
    """User to search for a shoppinglist"""
    @token_required
    def get(self, current_user):
        searchedlist=request.args.get("q") 
        shoppinglist = Shoppinglists.query.filter(Shoppinglists.shoppinglist_name.like('%'+searchedlist+'%')).first()
        shoplist = []
        if shoppinglist:
            p = Product.query.filter_by(shoppinglist=shoppinglist.shoppinglist_name).all()
            for i in p:
                produit = {}
                produit['Product'] = i.product
                produit['Amountspent'] = i.AmountSpent
                produit['Quantity'] = i.Quantity
                shoplist.append(produit)
            if len(shoplist)==0:
                return jsonify({'message':shoppinglist.shoppinglist_name+" Shoppinglist still empty"})
            else:
                return jsonify({'existing products of searched list':shoplist})
        else:
            return jsonify({'Message':'No list found'})

class SearchProduct(Resource):
    """User to search for a product"""
    @token_required
    def get(self, current_user):
        searchedProduct=request.args.get("q") 
        produit = Product.query.filter(Product.product.like('%'+searchedProduct.lower()+'%')).first()
        item = {}
        if produit:
            item['Product'] = produit.product
            item['Amountspent'] = produit.AmountSpent
            item['Quantity'] = produit.Quantity
            item['shoppinglist_name'] = produit.shoppinglist_id
        if len(item) ==0:
            return jsonify({'Message':"Product doesnt exist"})
        else:
            return jsonify({'Searched product':item})
        
class UserLogout(Resource):
    """User to logout"""
    @token_required
    def post(self, current_user):
        if current_user:
            session['loggedUser'] = None
            return jsonify({'message':'You are logout'})
        else:
            return jsonify({'message':'You must be login to logout'})

class GetUserShoppinglists(Resource):
    """API to return shoppinglists """
    @token_required
    def get(self, current_user):
        each_page = request.args.get("each_page") 
        page_number = request.args.get("page_number")
        user = session['loggedUser']
        shoppinglist = Shoppinglists.query.filter_by(user=user).paginate(per_page=int(each_page), page=int(page_number)).items
        output = []
        for p in shoppinglist:
            output.append(p.shoppinglist_name)
        return jsonify({'lists':output})

class GetUserShoppinglist(Resource):
    """API to return a given shoppinglist """
    @token_required
    def get(self, current_user, id):
        each_page = request.args.get("each_page") 
        page_number = request.args.get("page_number")
        Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id.lower()).first()
        output = []
        if Shoppinglist is not None:
            slist = Product.query.filter_by(shoppinglist=Shoppinglist.shoppinglist_name).paginate(per_page=int(each_page), page=int(page_number)).items
            if slist is not None:
                for s in slist:
                    produit = {}
                    produit['Product'] = s.product
                    produit['Amountspent'] = s.AmountSpent
                    produit['Quantity'] = s.Quantity
                    output.append(produit)
        if len(output)==0:
            return jsonify({'Message':"Shoppinglist is empty"})
        else:
            return jsonify({'Products':output})

class UpdateUserShoppinglist(Resource):
    """API to rename a given shoppinglist"""
    @token_required
    def put(self, current_user, id):
        data = request.get_json()
        newName = data.get('newName')
        if not newName:
            return jsonify({"message":"Missing information about the user"})
        else:  
            Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id.lower()).first()
            if Shoppinglist is not None:
                listofitems = Product.query.filter_by(shoppinglist=id)
                for l in listofitems:
                    l.shoppinglist = newName
                    l.register(l)
                Shoppinglist.shoppinglist_name = newName
            
                Shoppinglist.register(Shoppinglist)
                return jsonify({"Message":"The list name has been changed"})
            return jsonify({"Message":"list doesnt exist"})

class PostUserShoppinglist(Resource):
    """User to add shoppinglist"""
    @token_required
    def post(self, current_user):
        data = request.get_json()
        shoppinglist_name = data.get('newlist')
        if shoppinglist_name:
            user_id = session['loggedUser']
            format_shoppinglist_name=shoppinglist_name.lower()
            StoredShoppinglist = Shoppinglists.query.filter_by(user=user_id, shoppinglist_name=format_shoppinglist_name).first()
           
            if  not StoredShoppinglist:
                newShoppinglist = Shoppinglists(format_shoppinglist_name,user_id)
                newShoppinglist.register(newShoppinglist)
                return jsonify({shoppinglist_name:'created'})
            else:
                return jsonify({'Message':'lists exists'})
        else:
            return jsonify({'Message':'No new list name included'})

class DeleteUserShoppinglist(Resource):
    """User to delete shoppinglist"""
    @token_required
    def delete(self, current_user, id):
        
        Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id.lower()).first()
        if Shoppinglist:
            produit = Product.query.filter_by(shoppinglist=Shoppinglist)
            if produit:
                for p in produit:
                    produit.edit(p)
            Shoppinglist.edit(Shoppinglist)
            return jsonify({"Message":"The list name has been deleted"})
        return jsonify({"Message":"The list doesnt"})

class AddProduct(Resource):
    """User to add product to shoppinglist"""
    @token_required
    def post(self, current_user, id):
        shoppinglist_id = id
        data = request.get_json()
        product = data.get('product')
        quantity = data.get('Quantity')
        amountspent = data.get('Amountspent')
        if product and quantity and amountspent:
            StoredProduct=Product.query.filter_by(product=product.lower(),shoppinglist=shoppinglist_id).first()
            if StoredProduct:
                return jsonify({'message':'The product exists'})
            else:
                productToAdd = Product( quantity, amountspent, shoppinglist_id,product)
                
                productToAdd.register(productToAdd)
                return jsonify({'message':'The product has been added'})
        else:
            return jsonify({'message':'Incomplete information'})

class UpdateShoppinglist(Resource):
    """User to update shoppinglist product"""
    @token_required
    def put(self, current_user, id, item_id):
        data = request.get_json()
        uantity = data.get('Quantity')
        AmountSpent = data.get('AmountSpent')
        UpdateItem = Product.query.filter_by(product=item_id.lower()).first()
        if UpdateItem:
            UpdateItem.Quantity = uantity
            UpdateItem.AmountSpent = AmountSpent
            UpdateItem.register(UpdateItem)
            return jsonify({'message':'The product has been updated'})
        return jsonify({'message':'The product doesnt exist'})

class DeleteItem(Resource):
    """User to add item from the shoppinglist"""
    @token_required
    def delete(self, current_user, id, item_id):
        ItemToDelete = Product.query.filter_by(product=item_id.lower()).first()
        if ItemToDelete:
            ItemToDelete.edit(ItemToDelete)
            return jsonify({'message':'The product has been deleted'})
        return jsonify({'message':'The product doesnt exist'})

class RestPassword(Resource):
    """User to reset password"""
    @token_required
    def put(self, current_user):
        data = request.get_json()
        newpass = data.get('Newpassword')
        username = data.get('Username')
        passw = data.get('pass')
        if newpass and username and passw:
            user = User.query.filter_by(username=username,Password=passw).first()
            if user:
                user.Password = newpass
                user.user = username
                db.session.commit()
                return jsonify({'message':"Password has been reset"})
            return jsonify({'message':'Not a valid user'})
        else:
            return jsonify({'message':'Incomplete informarion'})

api.add_resource(DeleteUserShoppinglist, '/shoppinglists/<string:id>', methods=['DELETE'])
api.add_resource(UpdateUserShoppinglist, '/shoppinglists/<string:id>', methods=['PUT'])
api.add_resource(GetUserShoppinglist, '/shoppinglist/<id>/', methods=['GET'])
api.add_resource(PostUserShoppinglist, '/shoppinglists/', methods=['POST'])
api.add_resource(GetUserShoppinglists, '/shoppinglists/', methods=['GET'])
api.add_resource(RestPassword, '/auth/RestPassword/', methods=['PUT'])
api.add_resource(DeleteItem, '/shoppinglist/<id>/items/<item_id>', methods=['DELETE'])
api.add_resource(UpdateShoppinglist, '/shoppinglist/<id>/items/<item_id>', methods=['PUT'])
api.add_resource(AddProduct, '/shoppinglist/<string:id>/items/', methods=['POST'])
api.add_resource(Search, '/search/', methods=['GET'])
api.add_resource(SearchProduct, '/searchProduct/', methods=['GET'])
api.add_resource(UserLogout, '/auth/logout/', methods=['POST'])
api.add_resource(UserLogin, '/auth/login/', methods=['POST'])        
api.add_resource(AddNewUser, '/auth/register/', methods=['POST'])
