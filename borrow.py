import datetime
from flask import Flask, flash, render_template, redirect, request, url_for, escape, session, g
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import model
from forms import BorrowForm, SignUpForm, LoginForm
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.setup_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login"

# Reload the user object from the user ID stored in the session. 
@login_manager.user_loader
def load_user(user_id):
  return model.User.query.get(int(user_id))

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
@app.route("/login", methods=["GET","POST"])
@app.route("/login", methods = ["GET", "POST"])
def login():
  # update the last_login and number of logins everytime that the user logs into the db
  # dont allow user to re-login after they've done so
  form = LoginForm()
  if form.validate_on_submit():
    user = model.session.query(model.User).filter(model.User.email == form.email.data).first()
    user_password = user.password
   
    if user is not None:
      login_user(user)
      
      flash("logged in successfully")
      return redirect(url_for("index"))
    else:
      flash("Incorrect Password")
      return redirect("login")
    # if current_user.id
  return render_template("login.html", form=form)

# Logout user
@app.route("/logout")
def logout():
	# remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

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
	user_id = session.get("user_id", None)
	form = BorrowForm(product_id=product_id, lender_id=lender_id, user_id=user_id)

	if form.validate_on_submit():
		borrower_id = user_id
		lender_id = lender_id
		product_id = product_id
		date_wanted = datetime.datetime.strptime(form.start_date.data, "%d-%b-%Y")
		date_returned_est = datetime.datetime.strptime(form.end_date.data, "%d-%b-%Y")

		#optional message
		#message = request.form['message']
		#create query
		borrow_request = model.History(borrower_id=borrower_id, lender_id=lender_id, product_id=product_id,
										date_wanted=date_wanted, date_returned_est=date_returned_est)
		#Add the object to a session and commit it.
		model.session.add(borrow_request)
		model.session.commit()
		return redirect("/")
	else:
		flash("didn't work")

	library_item = model.session.query(model.Library).filter_by(product_id=product_id).first()
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