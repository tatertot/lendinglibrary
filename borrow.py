import datetime
from flask import Flask, flash, render_template, redirect, request, url_for, escape, session, g, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import model
from forms import BorrowForm, SignUpForm, LoginForm, SearchForm, AddProductForm, AddToLibraryForm
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user
from amazonproduct.api import API 
from lxml import etree
from lxml import objectify
import bottlenose
from amazon.api import AmazonAPI
from twilio.rest import TwilioRestClient
import logging, logging.handlers
import twilio

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
    return render_template("index.html", users=user_list, library=library, user_id=user_id)

# login as a user   
@app.route("/login", methods=["GET","POST"])
def login():
    # update the last_login and number of logins everytime that the user logs into the db
    # dont allow user to re-login after they've done so
    form = LoginForm()
    if form.validate_on_submit():
      user = model.session.query(model.User).filter(model.User.email == form.email.data).first()
      user_password = form.password.data
     
      if user is not None and user_password == user.password:
        login_user(user)
        
        #flash("logged in successfully")
        return redirect(url_for("dashboard"))
      else:
        flash("Incorrect Password")
        return redirect("login")
      # if current_user.id
    return render_template("login.html", form=form)


# Logout user
@app.route("/logout")
@login_required
def logout():
  logout_user()
  #flash("You are now logged out")
  return redirect(url_for("index"))


#signup form
@app.route('/sign_up', methods = ["POST","GET"])
def sign_up():
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


@app.route("/search", methods = ["POST","GET"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
      referrer = form.referrer.data
      query = form.query.data
      results = model.session.query(model.Library).filter(model.Library.product_desc.like('%'+ query + '%')).all()

      if not results:
        #redirect to new page with amazon search results
        return redirect(url_for('amz_search', query=query, referrer=referrer))
      else:
        for i in results:
            similar_products = None
            try:
                if i.product.asin:
                    asin = i.product.asin
                    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOC_TAG)
                
                    similar_root = api.similarity_lookup(asin, ResponseGroup='Large')
                    #~ from lxml import etree
                    #~ print etree.tostring(root, pretty_print=True)
                    nspace = similar_root.nsmap.get(None, '')
                    similar_products = similar_root.xpath('//aws:Items/aws:Item', 
                                 namespaces={'aws' : nspace})
            except:
                similar_products = None

            #render page with search results
            if referrer == 'dashboard':
                return render_template('results.html', results=results, similar_products=similar_products)
            else:
                form = AddProductForm()
                return render_template('add_product_results.html', results=results, similar_products=similar_products, form=form)


    return render_template("search.html", form=form)



@app.route("/dashboard")
@login_required
def dashboard():
    user_list = model.User.query.get(current_user.id)
    histories = model.session.query(model.History).filter_by(lender_id=current_user.id)
    borrowed = model.session.query(model.History).filter_by(borrower_id=current_user.id, date_returned = None)
    current_date = datetime.datetime.now()
    notifications = request_notifications()
    search_bar = search()

    return render_template("user_library.html", user=user_list, user_id=current_user.id, notifications=notifications, histories=histories, borrowed=borrowed,search=search_bar,current_date=current_date)
# user's lending library
# click on username and view list of producsts in their library

@app.route("/users")
@login_required
def user_library():
    user_list = model.session.query(model.User).all()
    
    return render_template("user_list.html",users=user_list)


# create borrow request
@app.route("/borrow/product/<int:product_id>/lender/<int:lender_id>", methods=["POST","GET"])
def borrow(product_id, lender_id):
    user_id = session.get("user_id", None)
    form = BorrowForm(product_id=product_id, lender_id=lender_id, user_id=user_id)

    if form.validate_on_submit():
        borrower_id = user_id
        lender_id = lender_id
        product_id = product_id
        date_wanted = datetime.datetime.strptime(form.start_date.data, "%d-%b-%Y")
        date_returned_est = datetime.datetime.strptime(form.end_date.data, "%d-%b-%Y")

        #create query
        borrow_request = model.History(borrower_id=borrower_id, lender_id=lender_id, product_id=product_id,
                                        date_wanted=date_wanted, date_returned_est=date_returned_est)
        #Add the object to a session and commit it.
        model.session.add(borrow_request)
        model.session.commit()
        return redirect("/dashboard")
    else:
        flash("didn't work")

    library_item = model.session.query(model.Library).filter_by(product_id=product_id).first()
    print library_item.id
    return render_template("borrow.html", library_item=library_item, user_id=user_id, lender_id=lender_id,form=form)


# accept contact's borrow request
def lend():
    pass


# list of products
def product_list():
    pass


# individual product page for editing 
def product(id):
    pass

@app.route("/add_product/<referrer>", methods = ["POST","GET"])
def add_product(referrer):
    form = AddProductForm()
    search_bar = search()

    if form.validate_on_submit():
        user_id = form.user_id.data
        name = form.name.data.strip()
        asin = form.asin.data.strip()
        category_id = form.category_id.data
        default_photo = form.default_photo.data.strip()
        custom_photo = form.custom_photo.data

        
        new_product = model.Product(name = name, 
                                    asin = asin, 
                                    category_id=category_id, 
                                    default_photo = default_photo, 
                                    custom_photo=custom_photo)
        new_product_id = new_product.id

        if referrer == 'new':
            model.session.add(new_product)
            model.session.commit()

        add_to_lib = model.Library(user_id=user_id, 
                                product_id=new_product_id,
                                product_desc=name,
                                status=1)
        model.session.add(add_to_lib)
        model.session.commit()

        return jsonify(msg='Success')
    else:
        if referrer=='new':
            return render_template("add_product.html", title="Add a Product", form=form, search=search_bar)
        else:
            return 'Fail'

@app.route("/add_to_library/", methods=["POST","GET"])    
def add_to_library():
    form = AddToLibraryForm(Form)

    if form.validate_on_submit():
        user_id = form.user_id.data
        product_id = form.product_id.data.strip()
        product_desc = form.product_desc.data.strip()
        status = 1
        new_product = model.Library(user_id=user_id, 
                                product_id=product_id,
                                product_desc=product_desc,
                                status=status)
        model.session.add(new_product)
        model.session.commit()
        return jsonify(msg='Success')
    else:
        return 'Fail'

# remove_product
def remove_product():
    pass


@app.route("/accept_request/<int:history_id>/<int:user_id>", methods=["POST","GET"])
def accept_request(history_id,user_id):
    request = model.History.query.get(history_id)
    request.date_borrowed = datetime.datetime.now()
    product = model.Library.query.filter_by(product_id=request.product_id).first()
    product.status = 2
    model.session.commit()
    return redirect(url_for('dashboard', user_id=user_id))


# user checks product back into their library
@app.route("/checkin_product/<int:history_id>/<int:user_id>", methods=["POST","GET"])
def checkin_item(history_id,user_id):
    request = model.History.query.get(history_id)
    request.date_returned = datetime.datetime.now()
    product = model.Library.query.get(request.product_id)
    product.status = 1
    model.session.commit()
    return redirect(url_for('dashboard', user_id=user_id))

def check_in_product():
    pass


@app.route("/notifications")
def request_notifications():
    #get request to borrow notifications 
    notifications = model.session.query(model.History).filter_by(lender_id=current_user.id, date_borrowed=None).all()

    #Syntax uses filter over filter_by because of comparison operators
    checked_out = model.session.query(model.History).filter(model.History.lender_id==current_user.id, model.History.date_borrowed >= 0, model.History.date_returned == None)
    current_date = datetime.datetime.now()

    return render_template("notifications.html", notifications=notifications, checked_out=checked_out, user_id=current_user.id, current_date=current_date)


CSRF_ENABLED = True
# set the secret key.  keep this really secret:
app.secret_key = 'banana banana banana'

#amazon key 
AWS_KEY = 'AKIAJQRVR67YSEDVVGJQ'
SECRET_KEY = '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'
ASSOC_TAG = 'boitba-20'

@app.route("/amazon/<query>")
def amazon(query):

    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOC_TAG)

    similar_root = api.similarity_lookup('B0058U6DQC', ResponseGroup='Large')

    #product_root = api.item_lookup('B0058U6DQC', ResponseGroup='Large')
    #product_root =  api.item_search(title='unicorn', ResponseGroup='Large')
    more_products = api.item_search('Books', Publisher='Galileo Press')
    #~ from lxml import etree
    #~ print etree.tostring(root, pretty_print=True)

    nspace = similar_root.nsmap.get(None, '')
    similar_products = similar_root.xpath('//aws:Items/aws:Item', 
                         namespaces={'aws' : nspace})

    # more_products = product_root.xpath('//aws:Items/aws:Item', 
    #                      namespaces={'aws' : nspace})

    return render_template("amazon.html", similar_products=similar_products, more_products = more_products, query=query)



# @app.route("/amazon_bottlenose")
# def amazon_bottlenose():
#     api = bottlenose.Amazon(AWS_KEY, SECRET_KEY, ASSOC_TAG)
#     root = api.SimilarityLookup(ItemId="B004VMAC8I", ResponseGroup="Images")
#     response = objectify.fromstring(root)
#     return render_template("amazon_bottlenose.html", response=response)

@app.route("/amz_search/<query>/<referrer>")
def amz_search(query,referrer):
    amazon = AmazonAPI(AWS_KEY, SECRET_KEY, ASSOC_TAG)
    products = amazon.search(Keywords=query, SearchIndex='All')
    if referrer == 'dashboard':
        return render_template("amz_search.html", products = products)
    else:
        form = AddProductForm()
        return render_template("amz_search_add.html", products = products, form=form)

@app.route("/app_results")
def app_results(query):
    amazon = AmazonAPI(AWS_KEY, SECRET_KEY, ASSOC_TAG)
    products = amazon.search(Keywords=query, SearchIndex='All')
    if referrer == 'dashboard':
        return render_template("amz_search.html", products = products)
    else:
        form = AddProductForm()
        return render_template("amz_search_add.html", products = products, form=form)



@app.route("/amazon_search")
def amazon_search():
    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOC_TAG)
    result = api.item_search('All',
        ResponseGroup='Large', AssociateTag='boitba-20', Keywords='tent marmot', ItemPage=2)

    total_results = result.results

    #item_search returns pages not items

    # extract paging information
    #total_results = result.results
    #Stotal_pages = len(result)  # or result.pages

    #~ from lxml import etree
    #~ print etree.tostring(root, pretty_print=True)
  

    return render_template("amazon_search.html", node = result, total_results=total_results)


@app.route("/checkin_product/<int:history_id>/<int:user_id>", methods=["POST","GET"])
def checkin_item(history_id,user_id):
    request = model.History.query.get(history_id)
    request.date_returned = datetime.datetime.now()
    product = model.Library.query.get(request.product_id)
    product.status = 1
    model.session.commit()
    return redirect(url_for('dashboard', user_id=user_id))


@app.route("/send_sms/<int:history_id>", methods=["POST"])
def send_sms(history_id):
    # Twilio AccountSid and AuthToken.
    # Twilio Number - 4156716511
    print history_id
    account_sid = 'AC23889a8a2f2d7e92e141f10b1265a53e'
    # SHHHH...Need to move tokens
    auth_token = 'a8c49ea47fa7a0cbbcc481f696833f8f'
    client = TwilioRestClient(account_sid, auth_token)
    history = model.History.query.get(history_id)
    print history.id, history_id
    borrower_num = history.borrower.phone_number
    borrower_num = "1" + borrower_num
    msg = "Hey ", history.borrower.fname, ", Please return ", history.lender.fname, "'s ", history.product.name,"."
    msg = ''.join(msg)

    message = client.sms.messages.create(to="+14153122776", from_="+14156716511",
                                         body=msg)
    if message.sid:
        return jsonify(history_id=history_id, msg='Message Sent')
    else:
        return jsonify(history_id=history_id, msg='SMS Failed, Please Try Again')

# @app.route("/return_rate")
# def return_rate(user_id):
#     #get the return history of user, num times item returned after return est/item numbers borrowed
#     items_returned = model.session.query(model.History).filter_by(lender_id=user_id).all()

#     return redirect(url_for('dashboard', user_id=user_id))
if __name__ == "__main__":
    app.run(debug = True)