from flask import Flask
from databases import *
from flask import Flask, url_for, flash, redirect, request, render_template
from flask import session as login_session


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


engine = create_engine('sqlite:///welcome_to_you.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


@app.route('/')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")	
	elif request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
		if email is None or password is None:
			flash("Missing Arguments")
			return redirect(url_for(login))
		if verify_password(email,password):
			member = session.query(member).filter_by(email = email).one()
			flash("Login Succesful, welcome %s" % member.name)
			login_session['name'] = member.name
			login_session['email'] = member.email
			login_session['id'] = member.id
			return redirect(url_for("inventory"))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for("login"))
@app.route('/recentPosts')
def viewRecentPosts():
	posts = session.query(Post).all()
	return render_template('recent_posts.html', posts = posts)


@app.route('/newMember', methods = ['GET','POST'])
def newMember():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        if name == "" or email == "" or password == "":
            flash("Your form is missing arguments")
            return redirect(url_for('newMember'))
        member = Member(name = name, email=email, address = address)
        member.hash_password(password)
        session.add(member)
        session.commit()
        flash("welcome new girl")
       
        if session.query(member).filter_by(email = email).first() is not None:

            flash("A user with this email address already exists")
            return redirect(url_for('newMember'))
        member = Member(name = name, email=email, address = address)
        member.hash_password(password)
        session.add(member)
        session.commit()
        flash("User Created Successfully!")
     
    else:
        return render_template('newMember.html')
        flash("User hasn't been created pleas sign up again")


@app.route('/postHere', methods = ['GET','POST'])
def postHere():
	if request.method == 'POST':
		status = request.form[status]
		#add to database --> Status()
		session.add()




@app.route("/product/<int:product_id>")
def product(product_id):
	product = session.query(product).filter_by(id = product_id).one()
	return render_template('product.html', product = product)

@app.route("/product/<int:product_id>/addToCart", methods = ['POST'])
def addToCart(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	quantity = request.form["quantity"]
	product = session.query(product).filter_by(id = product_id).one()
	shoppingcart = session.query(shoppingcart).filter_by(member_id = login_session["id"]).one()
	if product.name in [item.product.name for item in shoppingcart.products]:
		asoc = session.query(shoppingcartAssociation).filter_by(shoppingcart = shoppingcart).filter_by(product = product).one()
		asoc.quantity = int(asoc.quantity) + int(quantity)
		flash("successfully added to shoppingcart")
		return redirect(url_for('shoppingcart'))
	else:
		a = ShoppingcartAssociation(product = product, quantity = quantity)
		shoppingcart.products.append(a)
		session.add_all([a,product, shoppingcart])
		session.commit()
		flash("Successfully added to shopping cart")
		return redirect(url_for('shoppingcart'))

@app.route("/shoppingcart")
def shoppingcart():
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	shoppingcart = session.query(shoppingcart).filter_by(member_id = login_session['id']).one()
	return render_template("shopsingcart.html", shoppingcart = shoppingcart)

@app.route("/removeFromCart/<int:product_id>", methods = ['POST'])
def removeFromCart(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	shoppingCart = session.query(shoppingcart).filter_by(member_id=login_session['id']).one()
	association = session.query(ShoppingcartAssociation).filter_by(shoppingcart=shoppingcart).filter_by(product_id=product_id).one()
	session.delete(association)
	flash("item deleted succesfully")
	return redirect(url_for('shoppingcart'))	


@app.route("/updateQuantity/<int:product_id>", methods = ['POST'])
def updateQuantity(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to do this")
		return redirect(url_for('login'))
	quantity = request.form['quantity']
	if quantity == 0:
		return removeFromCart(product_id)
	if quantity < 0:
		flash("Can't store negative quantities .")
		return redirect(url_for('shoppingcart'))
	shoppingcart = session.query(Shoppingcart).filter_by(member_id=login_session['id']).one()
	assoc = session.query(shoppingcartAssociation).filter_by(shoppingcart=shoppingcart).filter_by(product_id=product_id).one()
	assoc.quantity = quantity
	session.add(assoc)
	session.commit()
	flash("Quantity Updated")
	return redirect(url_for('shoppingcart'))			

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	
	if 'id' not in login_session:
		flash("You must be logged in to actually checkout")
		return redirect(url_for('login'))
	shoppingcart = session.query(shoppingcart).filter_by(member_id=login_session['id']).one()
	if request.method == 'POST':
		order = Order(member_id=login_session['id'], confirmation=generateConfirmationNumber())
		order.total = calculateTotal(shoppingcart)
		
		for item in shoppingcart.products:
			assoc = OrdersAssociation(product=item.product, product_qty=item.quantity)
			order.products.append(assoc)
			session.delete(item)
		session.add_all([order, shoppingcart])
		session.commit()
		return redirect(url_for('confirmation', confirmation=order.confirmation))
	elif request.method == 'GET':
		return render_template('checkout.html', shoppingcart=shoppingcart, total="%.2f" % calculateTotal(shoppingcart))

def calculateTotal(shoppingcart):
	total = 0.0
	for item in shoppingcart.products:
		total += item.quantity * float(item.product.price)
	return total

def generateConfirmationNumber():
	return "".join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(16))

@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	if 'id' not in login_session:
		flash("you must be logged in tho confirm")
		return redirect (url_for('login'))
	order = session.query(Order).filter_by(confirmation=confirmation).one()
	photo_path = url_for('uploaded_file', filename=order.member.photo)
	return render_template('confirmation.html', order=order, photo_path=photo_path)


@app.route('/logout', methods = ['POST'])
def logout():
	if 'id' not in login_session:
		flash("you must be logged in to perform this action")
		return redirect (url_for('login'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("Logged Out Successfully")
	return redirect(url_for('inventory'))


@app.route('/')
@app.route('/inventory')
def inventory():
	items = session.query(product).all()
	return render_template('inventory.html', items=items)

def verify_password(email, password):
	member = session.query(member).filter_by(email=email).first()
	if not Member or not member.verify_password(password):
		return False
	g.member = member
	return True






@app.route('/aboutMe' , methods = ['GET'])
def aboutMe():
	items = session.query(info).all()
	return render_template('aboutMe.html', info=info)




def verify_password(email, password):
	member = session.query(member).filter_by(email = email).first()
	if not member or not member.verify_password(password):
		return False
	return True

	pass

if __name__ == '__main__':
	app.run(debug=True)