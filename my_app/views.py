from flask import render_template,Blueprint,request,redirect,url_for,session
from my_app.models import User,Product,ProductForm,LoginForm,Shoppinglists
from my_app import db,app
shoppinglist=Blueprint('shoppinglist',__name__)
@shoppinglist.route('/',methods=['POST','GET'])
def home():
    form=LoginForm(request.form,csrf_enabled=False)
    if request.method=='POST' and form.validate():
        UserName=request.form.get('UserName')
        LoginPassword=request.form.get('LoginPassword')
        users=User.query.filter_by(user=UserName).first()
        
        if users:
            if LoginPassword == users.Password:
                session['user']=users.user
                return redirect(url_for('shoppinglist.view'))
            else:
               
                redirect(url_for('shoppinglist.home'))
        else:
            
            redirect(url_for('shoppinglist.home'))
        
    return render_template('Login.html',form=form)
@shoppinglist.route('/signup',methods=['POST','GET'])
def signUp():
     if request.method=='POST':
        user=request.form.get('UserName')
        Surname=request.form.get('SecondName')
        Firstname=request.form.get('FirstName')
        email=request.form.get('Email')
        Password=request.form.get('Password')
        NewUser=User(user,Surname,Firstname,email,Password)
        db.session.add(NewUser)
        db.session.commit()
        return redirect(url_for('shoppinglist.home',))
     return render_template('Registeration.html')
@shoppinglist.route('/list')
def view():
    user=session['user']
    Usershoppinglist=Shoppinglists.query.filter_by(user_id=user).all()
    return render_template('ShoppingLists.html',shoppinglist=Usershoppinglist)
@shoppinglist.route('/addList/',methods=['POST','GET'])
def addShoppinglist():
    if request.method=='POST':
        name=request.form.get('shoppinglistname')
        user=session['user']
        AdList=Shoppinglists(user,name)
        db.session.add(AdList)
        db.session.commit()
        return redirect(url_for('shoppinglist.view'))
    return render_template('AddList.html')
@shoppinglist.route('/add/<shoppinglist_name>',methods=['POST','GET'])
def addProduct(shoppinglist_name):
    form=ProductForm(request.form,csrf_enabled=False)
    if request.method=='POST':
        product=request.form.get('product')
        Quantity=request.form.get('Quantity')
        AmountSpent=request.form.get('AmountSpent')
        shoppinglist_name=shoppinglist_name

        AddProduct=Product(product,Quantity,AmountSpent,shoppinglist_name)
        db.session.add(AddProduct)
        db.session.commit()
        return redirect(url_for('shoppinglist.Items',shoppinglist_name=shoppinglist_name))
        
    return render_template('AddProduct.html',form=form,shoppinglist_name=shoppinglist_name)
@shoppinglist.route('/delete/<itemid>/<shoppinglist_name>')
def deleteItem(itemid,shoppinglist_name):
    DeleteProduct=Product.query.filter_by(id=itemid).first()
    ProductName=DeleteProduct.product
    db.session.delete(DeleteProduct)
    db.session.commit()
    return redirect(url_for('shoppinglist.Items',shoppinglist_name=shoppinglist_name))
@shoppinglist.route('/update/<id>/<shoppinglist_name>',methods=['POST','GET'])
def updateItem(id,shoppinglist_name):
    if request.method=='POST':
        Item=Product.query.filter_by(id=id).first()
        Quantity=request.form.get('Quantity')
        AmountSpent=request.form.get('AmountSpent')
        Item.Quantity=Quantity
        Item.AmountSpent=AmountSpent
        db.session.add(Item)
        db.session.commit()
        return redirect(url_for('shoppinglist.Items',shoppinglist_name=shoppinglist_name))
    return render_template('UpdateItem.html',id=id,shoppinglist_name=shoppinglist_name)
@shoppinglist.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('shoppinglist.home'))
@shoppinglist.route('/products/<shoppinglist_name>',methods=['GET','POST'])
def Items(shoppinglist_name):
    if request.method=='POST':
        shoppinglist_name=request.form.get('shoppinglist_name')
        product=Product.query.filter_by(shoppinglist_id =shoppinglist_name).all()
        return render_template('ShoppingList.html',products=product,shoppinglist_name=shoppinglist_name)

    product=Product.query.filter_by(shoppinglist_id =shoppinglist_name).all()
    return render_template('ShoppingList.html',products=product,shoppinglist_name=shoppinglist_name)
@shoppinglist.route('/updateList/<id>/<shoppinglist_name>',methods=['GET','POST'])
def updateList(id,shoppinglist_name):
    if request.method=='POST':
        user=session['user']
        listtoupdate=Shoppinglists.query.filter_by(shoppinglist_name=shoppinglist_name,id=id).first()
        listtoupdate.shoppinglist_name=request.form.get('newname')
        db.session.add(listtoupdate)
        db.session.commit()
        Usershoppinglist=Shoppinglists.query.filter_by(user_id=user).all()
        return render_template('ShoppingLists.html',shoppinglist=Usershoppinglist)
    return render_template('updateList.html',id=id,shoppinglist_name=shoppinglist_name)
@shoppinglist.route('/deleteList/<id>/<shoppinglist_name>')
def deleteList(id,shoppinglist_name):
    SLdel=Shoppinglists.query.filter_by(id=id).first()
    db.session.delete(SLdel)
    db.session.commit()
    user=session['user']
    Usershoppinglist=Shoppinglists.query.filter_by(user_id=user).all()
    return render_template('ShoppingLists.html',shoppinglist=Usershoppinglist)

