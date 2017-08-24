from flask import Flask,request,jsonify,session
from flask_restful import Resource,Api
from my_app.models import User,Product,Shoppinglists
from my_app import db,app
from flask_httpauth import HTTPBasicAuth
auth=HTTPBasicAuth()

api=Api(app)

class AddNewUser(Resource):
    def post(self):
        user=request.json['user']
        Surname=request.json['Surname']
        Email=request.json['Email']
        Firstname=request.json['Firstname']
        Password=request.json['Password']
        NewUser=User(user,Surname,Firstname,Email,Password)
        db.session.add(NewUser)
        db.session.commit()
        return jsonify({'message':'User created'})
class UserLogin(Resource):


    def post(self):
        userName=request.json['user']
        UserPass=request.json['Password']
        users=User.query.filter_by(user=userName).first()
        if users:
            if UserPass == users.Password:
                session['user']=users.user
                session['pass']=users.Password
                shoppinglist=Shoppinglists.query.filter_by(user_id=users.user).all()
                output=[]
                for p in shoppinglist:
                    output.append(p.shoppinglist_name)
                return jsonify({'lists':output})
            else:
               
                return jsonify({'message':'Wrong password'})
        else:
            
            return jsonify({'message':'Not a user'})
class UserLogout(Resource):
    def post(self):
        session.pop('user')
        session.pop('pass')
        return jsonify({'message':'You are logout'})
class getUserShoppinglists(Resource):
   @auth.login_required
    def get(self):
        shoppinglist=Shoppinglists.query.filter_by(user_id=session['user']).all()
        output=[]
        for p in shoppinglist:
            output.append(p.shoppinglist_name)
        return jsonify({'lists':output})
class getUserShoppinglist(Resource):
    @auth.login_required
    def get(self,id):
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        slist=Product.query.filter_by(shoppinglist_id=Shoppinglist).all()
        output=[]
        for s in slist:
            produit={}
            produit['Product']=s.product
            produit['Amountspent']=s.AmountSpent
            produit['Quantity']=s.Quantity
            output.append(produit)
        return jsonify({'list':output})
class updateUserShoppinglist(Resource):
    @auth.login_required
    def put(self,id):
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        newName=request.json['newName']
        Shoppinglist.shoppinglist_name=newName
        db.session.add(Shoppinglist)
        db.session.commit()
        return jsonify({"Message":"The list name has been changed"})

class postUserShoppinglist(Resource):
    @auth.login_required
    def post(self):
        user_id=session['user']
        shoppinglist_name=request.json['newlist']
        newShoppinglist=Shoppinglists(user_id,shoppinglist_name)
        db.session.add(newShoppinglist)
        db.session.commit()
        return jsonify({shoppinglist_name:'created'})

class deleteUserShoppinglist(Resource):
    @auth.login_required
    def delete(self,id):
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        db.session.delete(Shoppinglist)
        db.session.commit()
        return jsonify({"Message":"The list name has been deleted"})
class AddProduct(Resource):
    @auth.login_required
    def post(self,id):
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        SL=Shoppinglist.shoppinglist_id
        p=request.json['product']
        Q=request.json['Quantity']
        A=request.json['Amountspent']
        Prod=Product(p,Q,A,SL)
        db.session.add(Prod)
        db.session.commit()
        return jsonify({'message':'The product has been added'})
    
class UpdateShoppinglist(Resource):
    @auth.login_required
    def put(self,id,item_id):
        Quantity=request.json['Quantity']
        AmountSpent=request.json['AmountSpent']
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        for s in Shoppinglist:
            if s.id is item_id:
                s.Quantity=Quantity
                s.AmountSpent=AmountSpent
        db.session.add(s)
        db.session.commit()
        return jsonify({'message':'The product has been updated'})
class DeleteItem(Resource):
    @auth.login_required
    def delete(self,id,item_id):
        Shoppinglist=Shoppinglists.query.filter_by(id=id).first()
        for s in Shoppinglist:
            if s.id is item_id:
                db.session.delete(s)
                db.session.commit()
        return jsonify({'message':'The product has been deleted'})
class RestPassword(Resource):
    @auth.login_required
    def put(self):
        username=request.json['Username']
        passw=request.json['pass']
        user=User.query.filter_by(user=username).first()
        newpass=request.json['Newpassword']
        user.Password=newpass
        user.user=username
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'The password is reset'})
api.add_resource(deleteUserShoppinglist,'/shoppinglists/<int:id>',methods=['DELETE'])
api.add_resource(updateUserShoppinglist,'/shoppinglists/<int:id>',methods=['PUT'])
api.add_resource(getUserShoppinglist,'/shoppinglists/<int:id>',methods=['GET'])
api.add_resource(postUserShoppinglist,'/shoppinglists/',methods=['POST'])
api.add_resource(getUserShoppinglists,'/shoppinglists/',methods=['GET'])
api.add_resource(RestPassword,'/auth/RestPassword/',methods=['PUT'])
api.add_resource(DeleteItem,'/shoppinglist/<int:id>/items/<int:item_id>',methods=['DELETE'])
api.add_resource(UpdateShoppinglist,'/shoppinglist/<int:id>/items/<int:item_id>',methods=['PUT'])
api.add_resource(AddProduct,'/shoppinglist/<int:id>/items/',methods=['POST'])
api.add_resource(UserLogout,'/auth/logout/')
api.add_resource(UserLogin,'/auth/login/',methods=['POST'])        
api.add_resource(AddNewUser,'/auth/register/',methods=['POST'])
if __name__ == '__main__':
    app.run(debug=True)
