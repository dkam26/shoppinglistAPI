from flask import Flask,request,jsonify,session,make_response
from flask_restful import Resource,Api
from my_app.models.models import User,Product,Shoppinglists,Store
from my_app import db,app,manager
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from functools import wraps
import datetime 

api=Api(app,catch_all_404s=True)
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing !'}),401
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            current_user=User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message':'Token is invalid !'}),401
        return f(current_user,*args,**kwargs) 
    return decorated

class AddNewUser(Resource):
    def post(self):
        user=request.json['user']
        Surname=request.json['Surname']
        Email=request.json['Email']
        Firstname=request.json['Firstname']
        Password=request.json['Password']
        hashed_password=generate_password_hash(Password,method='pbkdf2:sha256')
        NewUser=User(user,Surname,Firstname,Email,Password)
        db.session.add(User(user,Surname,Firstname,Email,Password))
        db.session.commit()
        return jsonify({'message':'User created'})
class UserLogin(Resource):


    def post(self):
        user=request.json['user']
        Password=request.json['Password']
        Users=User.query.filter_by(user=user,Password=Password).first()
        if Users:
            session['users']=Users.user
            session['Password']=Users.Password
            token=jwt.encode({'id':Users.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
            return jsonify({'Welcome':session['users'],'token':token.decode('UTF-8')})
        return jsonify({'message':'Wrong creditinals'})
class searchlist(Resource):
    @token_required
    def get(self,current_user,name):
        shoppinglist=Shoppinglists.query.filter_by(shoppinglist_name=name).first()
        shoplist=[]
        if shoppinglist:
            p=Product.query.filter_by(shoppinglist_id=shoppinglist.shoppinglist_name).all()
            for i in p:
                produit={}
                produit['Product']=i.product
                produit['Amountspent']=i.AmountSpent
                produit['Quantity']=i.Quantity
                shoplist.append(produit)
           
    
        return jsonify({'existing products of searched list':shoplist})
class searchProduct(Resource):
    @token_required
    def get(self,current_user,name):
        produit=Product.query.filter_by(product=name).first()
        if produit:
            item={}
            item['Product']=produit.product
            item['Amountspent']=produit.AmountSpent
            item['Quantity']=produit.Quantity
            item['shoppinglist_name']=produit.shoppinglist_id
        return jsonify({'Searched product':item})


class UserLogout(Resource):
    @token_required
    def post(self,current_user):
        session.pop('users')
        session.pop('Password')
        return jsonify({'message':'You are logout'})

class getUserShoppinglists(Resource):
    @token_required
    def get(self,current_user,number):
        user=session.get('users')
        shoppinglist=Shoppinglists.query.filter_by(user_id=user).paginate(1,number).items
        output=[]
        for p in shoppinglist:
            output.append(p.shoppinglist_name)
        return jsonify({'lists':output})
class getUserShoppinglist(Resource):
    @token_required
    def get(self,current_user,id,number):
        Shoppinglist=Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        slist=Product.query.filter_by(shoppinglist_id=Shoppinglist.shoppinglist_name).paginate(1,number).items
        output=[]
        for s in slist:
            produit={}
            produit['Product']=s.product
            produit['Amountspent']=s.AmountSpent
            produit['Quantity']=s.Quantity
            output.append(produit)
        return jsonify({'Products':output})
class updateUserShoppinglist(Resource):
    @token_required
    def put(self,current_user,id):
        Shoppinglist=Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        newName=request.json['newName']
        Shoppinglist.shoppinglist_name=newName
        store=Store()
        store.register(Shoppinglist)
        return jsonify({"Message":"The list name has been changed"})

class postUserShoppinglist(Resource):
    @token_required
    def post(self,current_user):
        shoppinglist_name=request.json['newlist']
        user_id=session.get('users')
        newShoppinglist=Shoppinglists(user_id,shoppinglist_name)
        store=Store()
        store.register(newShoppinglist)
        return jsonify({shoppinglist_name:'created'})

class deleteUserShoppinglist(Resource):
    @token_required
    def delete(self,current_user,id):
        Shoppinglist=Shoppinglists.query.filter_by(shoppinglist_name=id).first()
        products=Product.query.filter_by(shoppinglist_id=id).first()
        store=Store()
        store.edit(Shoppinglist)
        store.edit(products)
        return jsonify({"Message":"The list name has been deleted"})
class AddProduct(Resource):
    @token_required
    def post(self,current_user,id):
        shoppinglist_id=id
        p=request.json['product']
        Q=request.json['Quantity']
        A=request.json['Amountspent']
        Prod=Product(p,Q,A,shoppinglist_id)
        store=Store()
        store.register(Prod)
        return jsonify({'message':'The product has been added'})
    
class UpdateShoppinglist(Resource):
    @token_required
    def put(self,current_user,item_id):
        Quantity=request.json['Quantity']
        AmountSpent=request.json['AmountSpent']
        UpdateItem=Product.query.filter_by(product=item_id).first()
        UpdateItem.Quantity=Quantity
        UpdateItem.AmountSpent=AmountSpent
        store=Store()
        store.register(UpdateItem)
        
        return jsonify({'message':'The product has been updated'})
class DeleteItem(Resource):
    @token_required
    def delete(self,current_user,item_id):
        ItemToDelete=Product.query.filter_by(product=item_id).first()
        store=Store()
        store.edit(ItemToDelete)
        return jsonify({'message':'The product has been deleted'})
class RestPassword(Resource):
    @token_required
    def put(self,current_user):
        newpass=request.json['Newpassword']
        username=request.json['Username']
        passw=request.json['pass']
        user=User.query.filter_by(user=username).first()
        user.Password=newpass
        user.user=username
        store=Store()
        store.edit(user)
        
        return jsonify({'message':'The password is reset'})
api.add_resource(deleteUserShoppinglist,'/shoppinglists/<id>',methods=['DELETE'])
api.add_resource(updateUserShoppinglist,'/shoppinglists/<id>',methods=['PUT'])
api.add_resource(getUserShoppinglist,'/shoppinglist/<id>/<int:number>',methods=['GET'])
api.add_resource(postUserShoppinglist,'/shoppinglists/',methods=['POST'])
api.add_resource(getUserShoppinglists,'/shoppinglists/<int:number>',methods=['GET'])
api.add_resource(RestPassword,'/auth/RestPassword/',methods=['PUT'])
api.add_resource(DeleteItem,'/shoppinglist/<id>/items/<int:item_id>',methods=['DELETE'])
api.add_resource(UpdateShoppinglist,'/shoppinglist/<id>/items/<item_id>',methods=['PUT'])
api.add_resource(AddProduct,'/shoppinglist/<string:id>/items/',methods=['POST'])
api.add_resource(searchlist,'/searchlist/<string:name>',methods=['GET'])
api.add_resource(searchProduct,'/searchProduct/<string:name>',methods=['GET'])
api.add_resource(UserLogout,'/auth/logout/')
api.add_resource(UserLogin,'/auth/login/',methods=['POST'])        
api.add_resource(AddNewUser,'/auth/register/',methods=['POST'])

if __name__=="__main__":
    manager.run()

