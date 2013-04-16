from flask import Flask, render_template, redirect, request, url_for, escape, session
import model

app = Flask(__name__)

@app.route("/")
def index():
	user_list = model.session.query(model.User).all()
	library = model.session.query(model.Library).filter_by(user_id=1)
	return render_template("user_list.html", users=user_list, library=library)


"""
def sign_up():
	pass

def create_user():
	pass

def login():
	pass

def logout():
	pass

def authenticate():
	pass

def users():
	pass

def library():
	pass

def borrow():
	pass

def lend():
	pass

def product_list():
	pass

def product(id):
	pass






"""

if __name__ == "__main__":
	app.run(debug = True)