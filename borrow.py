import datetime
from flask import Flask, flash, render_template, redirect, request, url_for, escape, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import model
from forms import BorrowForm, SignUpForm
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user

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

#signup form
@app.route('/sign_up', methods = ["POST","GET"])
def form():
  form = SignUpForm()
  if form.validate_on_submit():
    user = model.session.query(model.User).filter(model.User.email == form.email.data).first()
    if user != None:
      user_email = user.email
      if user_email == form.email.data:
        flash ("email already exists")
        return redirect(url_for("form"))
    if user == None:
      fname = form.fname.data
      lname = form.lname.data
      email = form.email.data
      password = form.password.data
      new_user = model.User(id = None,
                            email=email,
                            password=password,
                            fname=fname,
                            lname=lname)
      model.session.add(new_user)
      model.session.commit()
      return redirect("/")
  return render_template("sign_up.html", title="Sign Up Form", form=form)



# user's lending library
# click on username and view list of producsts in their library
def user_library():
	pass

# create borrow request
@app.route("/borrow/<int:product_id>/<int:lender_id>", methods=["POST","GET"])
def borrow(product_id, lender_id):
	form = BorrowForm()
	user_id = session.get("user_id", None)

# @app.route("/borrow_request", methods=['GET','POST'])
# def borrow_request():
# 	form = BorrowForm()
	# if request.method == 'POST' and form.validate():
	# 	borrow
	if form.validate_on_submit():
		borrower_id = form.user_id.data
		lender_id = form.lender_id.data
		product_id = form.product_id.data
		date_wanted = datetime.datetime.strptime(form.start_date.data, "%d-%b-%Y")
		date_returned_est = datetime.datetime.strptime(form.end_date.data, "%d-%b-%Y")


		#optional message
		#message = request.form['message']
		#create query
		borrow_request = model.History(borrower_id=borrower_id, lender_id=lender_id, product_id=product_id)
		#Add the object to a session and commit it.
		model.session.add(borrow_request)
		model.session.commit()
		return redirect("/")
	else:
		flash("didn't work")

	library_item = model.session.query(model.Library).filter_by(product_id= product_id).first()
	return render_template("borrow.html", library_item=library_item, user_id=user_id, form=form)

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

CSRF_ENABLED = True
# set the secret key.  keep this really secret:
app.secret_key = 'banana banana banana'

if __name__ == "__main__":
	app.run(debug = True)