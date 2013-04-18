from flask import Flask, flash, render_template, redirect, request, url_for, escape, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import model

app = Flask(__name__)

# class BorrowRequest(Form):
# 	#get borrower id
# 	borrower_id = HiddenField('borrower_id')
# 	#get lender id
# 	lender_id = HiddenField('lender_id')
# 	#get product id
# 	product_id = HiddenField('product_id')
# 	#get request date
# 	date_requested = HiddenField['date_requested']
# 	#get date producted is wanted
# 	date_wanted = TextField['start_date']
# 	#get date producted is going to be returned
# 	date_wanted = TextField['end_date']


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
@app.route("/logout")
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
	user_id = session.get("user_id", None)
	library_item = model.session.query(model.Library).filter_by(product_id = product_id).first()
	return render_template("borrow.html", library_item = library_item, user_id=user_id)

@app.route("/borrow_request", methods=['POST'])
def borrow_request():
	# form = BorrowRequest(request.form)
	# if request.method == 'POST' and form.validate():
	# 	borrow

	#get borrower id
	borrower_id = request.form['user_id']
	#get lender id
	lender_id = request.form['lender_id']
	#get product id
	product_id = request.form['product_id']
	#get request date
	#get date producted is wanted
	#date_wanted = request.form['start_date']
	#date_wanted_format = model.datetime.datetime.strptime(date_wanted, "%d-%b-%Y")
	#get date producted is going to be returned
	#date_returned_est = request.form['end_date']
	#date_returned_est_format = model.datetime.datetime.strptime(date_returned_est, "%d-%b-%Y")
	#optional message
	#message = request.form['message']
	#create query
	borrow_request = model.History(borrower_id = borrower_id, lender_id = lender_id, product_id = product_id)
	#add the object to a session
	model.session.add(borrow_request)
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