from flask import Flask, flash, render_template, redirect, request, url_for, escape, session
import model

app = Flask(__name__)

@app.route("/")
def index():
	user_id = session.get("user_id", None)
	user_list = model.session.query(model.User).all()
	library = model.session.query(model.Library).filter_by(user_id=1)
	return render_template("user_list.html", users=user_list, library=library, user_id=user_id)


# User sign up
def sign_up():
	pass

# login as a user 	
@app.route("/login")
def login():
	return render_template("login.html")

# Logout user
def logout():
	# remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

#authenticate user
@app.route("/authenticate", methods=["POST"])
def authenticate():
	email = request.form['email']
	password = request.form['password']
	# capture the userid information from model-database
	user_query = model.session.query(model.User).filter_by(email=email,password=password)
	if user_query.first():
		user = user_query.first()
		# after getting the session variable back, you have to point it to a page
		session['user_id'] = user.id
		return redirect("/")
	else:
		flash("Incorrect Email/Password Combo. Please try again.")
		return redirect("/login")

# view contact list
def users():
	pass

# user's lending library
# click on username and view list of producsts in their library
def user_library():
	pass

# create borrow request
@app.route("/borrow/<int:product_id>/<int:lender_id>", methods=["GET"])
def borrow(product_id, lender_id):
	#ind_rating = model.session.query(model.Rating).filter_by(user_id = user_id, movie_id = movie_id).first()
	return render_template("borrow.html")

@app.route("/borrow_request", methods=["POST"])
def borrow_request():
	#get borrower id
	borrower_id = request.form['borrower_id']
	#get lender id
	lender_id = request.form['lender_id']
	#get product id
	product_id = request.form['product_id']
	#get request date
	date_requested = request.form['date_requested']
	#get date producted is wanted
	date_wanted = request.form['date_request']

	#create query
	request = model.History(borrower_id = borrower_id, lender_id = lender_id, product_id = product_id, date_requested=date_requested, date_wanted=date_wanted)
	#add the object to a session
	model.session.add(request)
    #commit session
	model.session.commit()
	return redirect("/")

# accept contact's borrow request
def lend():
	pass

# list of products
def product_list():
	pass

# individual product page for editing 
def product(id):
	pass

# add product
def add_product():
	pass

# remove_product
def remove_product():
	pass

# return_product
def return_product():
	pass

# user checks product back into their library
def check_in_product():
	pass
# set the secret key.  keep this really secret:
app.secret_key = 'banana banana banana'

if __name__ == "__main__":
	app.run(debug = True)