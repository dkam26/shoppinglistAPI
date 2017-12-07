from flask import Flask, request, jsonify, session, make_response
from flask_restful import Resource, Api
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from my_app.models.models import User, Product, Shoppinglists, Store
from my_app import db, app

api = Api(app, catch_all_404s=True)
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
        user = request.json['user']
        surname = request.json['Surname']
        email = request.json['Email']
        firstname = request.json['Firstname']
        password = request.json['Password']
        #To confirm if all the required info is submitted
        if not user or not surname or not email or not firstname or not password:
            return jsonify({"message":"Missing information about the user"})
        else:
            existing_user = User.query.filter_by(user=user).first()
            existing_email = User.query.filter_by(email=email).first()
            if existing_email is None and existing_user is None:
                #New user to be registered
                newUser=User(user, surname, firstname, email, password)
                db.session.add(newUser)
                db.session.commit()
                return jsonify({'message':'User created'})
            else:
                return jsonify({'message':"User exists"})
class UserLogin(Resource):
    """User to login"""
    def post(self):
        user = request.json['user']
        password = request.json['Password']
        users = User.query.filter_by(user=user, Password=password).first()
        #confirm the User is registered
        if users:
            session['loggedUser'] = users.user
            token = jwt.encode({
                'id':users.id,
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
                }, app.config['SECRET_KEY'])
            return jsonify({'Welcome':session['loggedUser'] , 'token':token.decode('UTF-8')})
        return jsonify({'message':'Wrong creditinals'})
class Searchlist(Resource):
    @token_required
    def get(self, current_user, name):
        shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=name).first()
        shoplist = []
        if shoppinglist:
            p = Product.query.filter_by(shoppinglist_id=shoppinglist.shoppinglist_name).all()
            for i in p:
                produit = {}
                produit['Product'] = i.product
                produit['Amountspent'] = i.AmountSpent
                produit['Quantity'] = i.Quantity
                shoplist.append(produit)
        return jsonify({'existing products of searched list':shoplist})
class SearchProduct(Resource):
    @token_required
    def get(self, current_user, name):
        produit = Product.query.filter_by(product=name).first()
        item = {}
        if produit:
            item['Product'] = produit.product
            item['Amountspent'] = produit.AmountSpent
            item['Quantity'] = produit.Quantity
            item['shoppinglist_name'] = produit.shoppinglist_id
        return jsonify({'Searched product':item})
class UserLogout(Resource):
    @token_required
    def post(self, current_user):
        if current_user:
            session['loggedUser'] = None
            return jsonify({'message':'You are logout'})
        else:
            return jsonify({'message':'You must be login to logout'})

class GetUserShoppinglists(Resource):
    @token_required
    def get(self, current_user, number):
        user = session['loggedUser']
        shoppinglist = Shoppinglists.query.filter_by(user_id=user).paginate(1, number).items
        output = []
        for p in shoppinglist:
            output.append(p.shoppinglist_name)
        return jsonify({'lists':output})
class GetUserShoppinglist(Resource):
    @token_required
    def get(self, current_user, id, number):
        Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        output = []
        if Shoppinglist is not None:
            slist = Product.query.filter_by(shoppinglist_id=Shoppinglist.shoppinglist_name).paginate(1, number).items
            if slist is not None:
                for s in slist:
                    produit = {}
                    produit['Product'] = s.product
                    produit['Amountspent'] = s.AmountSpent
                    produit['Quantity'] = s.Quantity
                    output.append(produit)
        return jsonify({'Products':output})
class UpdateUserShoppinglist(Resource):
    @token_required
    def put(self, current_user, id):
        store = Store()
        newName = request.json['newName']
        Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        if Shoppinglist is not None:
            listofitems = Product.query.filter_by(shoppinglist_id=id)
            for l in listofitems:
                l.shoppinglist_id = newName
                store.register(l)
            Shoppinglist.shoppinglist_name = newName
            store.register(Shoppinglist)
            return jsonify({"Message":"The list name has been changed"})
        return jsonify({"Message":"list doesnt exist"})

class PostUserShoppinglist(Resource):
    @token_required
    def post(self, current_user):
        shoppinglist_name = request.json['newlist']
        if shoppinglist_name:
            user_id = session['loggedUser']
            newShoppinglist = Shoppinglists(shoppinglist_name,user_id)
            store = Store()
            store.register(newShoppinglist)
            return jsonify({session['loggedUser']:'created'})
        else:
            return jsonify({'Message':'No new list name included'})

class DeleteUserShoppinglist(Resource):
    @token_required
    def delete(self, current_user, id):
        store = Store()
        Shoppinglist = Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        if Shoppinglist:
            store.edit(Shoppinglist)
            return jsonify({"Message":"The list name has been deleted"})
        return jsonify({"Message":"The list doesnt"})
class AddProduct(Resource):
    @token_required
    def post(self, current_user, id):
        shoppinglist_id = id
        product = request.json['product']
        quantity = request.json['Quantity']
        amountspent = request.json['Amountspent']
        productToAdd = Product(product, quantity, amountspent, shoppinglist_id)
        store = Store()
        store.register(productToAdd)
        return jsonify({'message':'The product has been added'})
class UpdateShoppinglist(Resource):
    @token_required
    def put(self, current_user, id, item_id):
        uantity = request.json['Quantity']
        AmountSpent = request.json['AmountSpent']
        UpdateItem = Product.query.filter_by(product=item_id).first()
        UpdateItem.Quantity = uantity
        UpdateItem.AmountSpent = AmountSpent
        store = Store()
        store.register(UpdateItem)
        return jsonify({'message':'The product has been updated'})
class DeleteItem(Resource):
    @token_required
    def delete(self, current_user, id, item_id):
        ItemToDelete = Product.query.filter_by(product=item_id).first()
        store = Store()
        store.edit(ItemToDelete)
        return jsonify({'message':'The product has been deleted'})
class RestPassword(Resource):
    @token_required
    def put(self, current_user):
        newpass = request.json['Newpassword']
        username = request.json['Username']
        passw = request.json['pass']
        user = User.query.filter_by(user=username,Password=passw).first()
        if user:
            user.Password = newpass
            user.user = username
            db.session.commit()
            #store = Store()
            #store.register(newuser)
            #store.edit(user)
            return jsonify({'message':user.Password})
        return jsonify({'message':'Not a valid user'})
api.add_resource(DeleteUserShoppinglist, '/shoppinglists/<string:id>', methods=['DELETE'])
api.add_resource(UpdateUserShoppinglist, '/shoppinglists/<string:id>', methods=['PUT'])
api.add_resource(GetUserShoppinglist, '/shoppinglist/<id>/<int:number>', methods=['GET'])
api.add_resource(PostUserShoppinglist, '/shoppinglists/', methods=['POST'])
api.add_resource(GetUserShoppinglists, '/shoppinglists/<int:number>', methods=['GET'])
api.add_resource(RestPassword, '/auth/RestPassword/', methods=['PUT'])
api.add_resource(DeleteItem, '/shoppinglist/<id>/items/<item_id>', methods=['DELETE'])
api.add_resource(UpdateShoppinglist, '/shoppinglist/<id>/items/<item_id>', methods=['PUT'])
api.add_resource(AddProduct, '/shoppinglist/<string:id>/items/', methods=['POST'])
api.add_resource(Searchlist, '/searchlist/<string:name>', methods=['GET'])
api.add_resource(SearchProduct, '/searchProduct/<string:name>', methods=['GET'])
api.add_resource(UserLogout, '/auth/logout/', methods=['POST'])
api.add_resource(UserLogin, '/auth/login/', methods=['POST'])        
api.add_resource(AddNewUser, '/auth/register/', methods=['POST'])

if __name__ == "__main__":
    app.run()
